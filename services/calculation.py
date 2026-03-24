import json
import os
from typing import List, Optional
from models.data_models import CleaningData, CleaningType, CalculationRequest, CalculationResult, CostParameters
from models.company_settings import CompanySettings
from core.database import get_db
import streamlit as st
import os
import json

class CalculationService:
    SETUP_TIME_PERCENTAGE = 0.10  # 10%

    def _get_company_settings(self):
        db = next(get_db())
        try:
            settings = db.query(CompanySettings).first()
            if not settings:
                from core.init_db import init_default_company_settings
                init_default_company_settings() # Auto-init
                settings = db.query(CompanySettings).first()
                if not settings:
                    # Fallback object if DB fails hard (Mock)
                    settings = CompanySettings(
                        hourly_rate=25.0,
                        vat_rate=19.0,
                        profit_margin=15.0,
                        setup_time_percentage=10.0
                    )
            return settings
        except Exception as e:
            print(f"DB Settings Error: {e}")
            # Robustness fallback
            return CompanySettings(
                hourly_rate=25.0, 
                vat_rate=19.0, 
                profit_margin=15.0, 
                setup_time_percentage=10.0
            )
        finally:
            db.close()
    
    def calculate_with_setup(self, area, service_type, base_price_per_m2):
        # ... (keep existing)
        base_total = area * base_price_per_m2
        setup_cost = base_total * self.SETUP_TIME_PERCENTAGE
        total = base_total + setup_cost
        
        return {
            "area_m2": area,
            "service_type": service_type,
            "base_price": round(base_total, 2),
            "setup_cost": round(setup_cost, 2),
            "total_price": round(total, 2),
            "price_per_m2": round(total / area, 2)
        }

    def __init__(self, data_path: str = "data/cleaning_data.json"):
        self.data_path = data_path
        self.data: CleaningData = self._load_data(self.data_path)

    # ... (keep static methods) ...
    @staticmethod
    @st.cache_resource
    def get_instance():
        return CalculationService()

    @staticmethod
    @st.cache_data(show_spinner=False, ttl=3600)
    def _load_data(data_path: str) -> CleaningData:
        try:
             # Construct absolute path if relative path is provided
            if not os.path.isabs(data_path):
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                data_path = os.path.join(base_dir, data_path)
            
            with open(data_path, 'r', encoding='utf-8') as f:
                data_dict = json.load(f)
                
            return CleaningData(**data_dict)
        except Exception as e:
            print(f"Error loading data from {data_path}: {e}")
            raise

    # ... (keep getters) ...
    def get_cleaning_types(self) -> List[CleaningType]:
        return self.data.cleaning_types

    def get_unique_categories(self) -> List[str]:
        return sorted(list(set(ct.category for ct in self.data.cleaning_types)))

    def get_types_by_category(self, category: str) -> List[CleaningType]:
        return [ct for ct in self.data.cleaning_types if ct.category == category]

    def get_cleaning_type_by_id(self, type_id: str) -> Optional[CleaningType]:
        for ct in self.data.cleaning_types:
            if ct.id == type_id:
                return ct
        return None

    def calculate_price(self, request: CalculationRequest) -> CalculationResult:
        cleaning_type = self.get_cleaning_type_by_id(request.cleaning_type_id)
        if not cleaning_type:
            raise ValueError(f"Cleaning type with ID {request.cleaning_type_id} not found.")

        # Load params from JSON first
        params = self.data.cost_parameters
        
        # OVERRIDE with DB Settings
        db_settings = self._get_company_settings()
        if db_settings:
            params.wage_per_hour = float(db_settings.hourly_rate)
            params.target_margin_percent = float(db_settings.profit_margin)
            params.setup_time_percent = float(db_settings.setup_time_percentage)
            # VAT used later
        
        # 1. Base Price Calculation
        # Use average base price and performance for calculation
        base_price_sqm = cleaning_type.base_price_per_sqm.avg
        performance_sqm_h = cleaning_type.performance_sqm_per_h.avg

        # 2. Apply Factors
        region_factor = params.regional_factors.get(request.region, 1.0)
        dirt_factor = params.dirt_factors.get(request.dirt_level, 1.0)
        
        # Adjust perfromance based on dirt level (dirtier = slower)
        adjusted_performance = performance_sqm_h / dirt_factor
        
        estimated_hours = request.area_sqm / adjusted_performance

        # 3. Calculate Costs
        # Rüstzeit hinzufügen (Task 2.1)
        setup_time_hours = estimated_hours * (params.setup_time_percent / 100)
        total_hours = estimated_hours + setup_time_hours

        # Labor-Cost basierend auf TOTAL hours
        labor_cost = total_hours * params.wage_per_hour * params.wage_overhead_factor
        
        # Material cost as percentage of labor cost
        material_cost = labor_cost * (params.material_markup_percent / 100)
        
        travel_cost = request.distance_km * params.travel_cost_per_km

        # Addons (Stone cleaning specifics)
        addon_costs = 0.0
        for addon_name in request.selected_addons:
            for addon_def in cleaning_type.addons:
                if addon_def.name == addon_name:
                    if addon_def.price_addition_per_sqm:
                        addon_costs += addon_def.price_addition_per_sqm * request.area_sqm
                    elif addon_def.price_factor:
                        labor_cost *= addon_def.price_factor

        # 4. Total Cost & Margin
        subtotal_cost = labor_cost + material_cost + travel_cost + addon_costs
        
        overhead_cost = subtotal_cost * (params.overhead_percent / 100)
        total_cost = subtotal_cost + overhead_cost
        
        # Margin calculation
        target_margin_decimal = params.target_margin_percent / 100
        net_price = total_cost / (1 - target_margin_decimal)
        
        margin_amount = net_price - total_cost

        # 5. Finalize
        # Use DB VAT if available
        vat_rate = db_settings.vat_rate if db_settings else 19.0
        gross_price = net_price * (1 + (vat_rate / 100))

        return CalculationResult(
            total_price_net=round(net_price, 2),
            total_price_gross=round(gross_price, 2),
            price_per_sqm=round(net_price / request.area_sqm, 2) if request.area_sqm > 0 else 0,
            estimated_hours=round(estimated_hours, 2),
            labor_cost=round(labor_cost, 2),
            material_cost=round(material_cost, 2),
            overhead_cost=round(overhead_cost, 2),
            travel_cost=round(travel_cost, 2),
            margin=round(margin_amount, 2),
            details={
                "base_performance_sqm_h": performance_sqm_h,
                "adjusted_performance_sqm_h": round(adjusted_performance, 2),
                "setup_time_hours": round(setup_time_hours, 2),
                "total_hours_with_setup": round(total_hours, 2),
                "region_factor": region_factor,
                "dirt_factor": dirt_factor,
            }
        )

    def calc_express(self, area: float, service_type: str) -> dict:
        avg_prices = {
            "Büroreinigung": 1.50,
            "Baureinigung (Grob)": 4.00,
            "Baureinigung (Fein)": 6.50,
            "Grundreinigung": 5.00,
            "Glasreinigung": 2.50,
            "Sanitärreinigung": 8.00,
            "Pflaster-/Verkehrsflächenreinigung": 3.20,
            "Steinreinigung/Naturstein": 12.00
        }
        # Fallback handling for prompt variations
        key = service_type
        if "Büro" in service_type: key = "Büroreinigung"
        
        base = area * avg_prices.get(key, 2.00)
        margin = base * 0.15
        return {
            "min": round(base - margin, 2),
            "center": round(base, 2),
            "max": round(base + margin, 2)
        }

    def check_plausibility(self, type_id: str, value: float, mode: str = "price") -> dict:
        """
        Checks if a given value (price or performance) is plausible for the cleaning type.
        mode: "price" (value in €/sqm) or "performance" (value in sqm/h)
        """
        cleaning_type = self.get_cleaning_type_by_id(type_id)
        if not cleaning_type:
            return {"is_plausible": False, "message": "Reinigungstyp nicht gefunden.", "level": "error"}

        if mode == "price":
            # Check Price Reference
            ref = cleaning_type.base_price_per_sqm
            # Allow some tolerance, e.g. -20% to +50% of the range
            min_valid = ref.min * 0.8
            max_valid = ref.max * 1.5
            
            if value < min_valid:
                return {
                    "is_plausible": False, 
                    "message": f"⚠️ Preis {value:.2f}€ liegt deutlich unter dem Standard ({ref.min:.2f}€ - {ref.max:.2f}€). Gefahr von Unterdeckung!", 
                    "level": "warning"
                }
            elif value > max_valid:
                return {
                    "is_plausible": False, 
                    "message": f"⚠️ Preis {value:.2f}€ liegt deutlich über dem Standard ({ref.min:.2f}€ - {ref.max:.2f}€). Gefahr der Ablehnung!", 
                    "level": "warning"
                }
            return {"is_plausible": True, "message": "Preis ist plausibel.", "level": "success"}
            
        elif mode == "performance":
            # Check Performance Reference
            ref = cleaning_type.performance_sqm_per_h
            min_valid = ref.min * 0.8
            max_valid = ref.max * 1.2
            
            if value < min_valid:
                 return {
                    "is_plausible": False, 
                    "message": f"⚠️ Leistung {value:.1f} m²/h ist sehr niedrig (Standard: {ref.min}-{ref.max}).", 
                    "level": "info"
                }
            elif value > max_valid:
                 return {
                    "is_plausible": False, 
                    "message": f"⚠️ Leistung {value:.1f} m²/h ist sehr hoch (Standard: {ref.min}-{ref.max}). Qualitätsprobleme möglich!", 
                    "level": "warning"
                }
            return {"is_plausible": True, "message": "Leistung ist plausibel.", "level": "success"}
            
        return {"is_plausible": False, "message": "Ungültiger Modus", "level": "error"}

@st.cache_resource
def get_calculation_service_v2():
    """Singleton CalculationService mit Streamlit Cache (V2)."""
    return CalculationService()

@st.cache_data(ttl=3600)
def calculate_price_cached(request_dict: dict) -> dict:
    # Use the new standalone function or get_instance
    service = get_calculation_service_v2()
    request = CalculationRequest(**request_dict)
    result = service.calculate_price(request)
    return result.model_dump()


