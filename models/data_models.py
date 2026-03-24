from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union

class ProjectDraft(BaseModel):
    id: Optional[int] = None
    name: str = "Unbenannter Entwurf"
    updated_at: datetime = Field(default_factory=datetime.now)
    data_json: str # Serialized full project data
    
# SQLAlchemy Model for Drafts
from core.database import Base

class ProjectDraftDB(Base):
    __tablename__ = "project_drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, default="default_user") # Placeholder for auth
    name = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    data_json = Column(Text) # Stores the JSON of the entire calculation/project state

from typing import List, Optional, Dict, Union

# --- Master Data Models ---

class CompanySettings(BaseModel):
    firmenname: str = ""
    standort: str = ""
    # Add other fields as needed

class WageParameters(BaseModel):
    stundenlohn_unterhaltsreinigung: float
    stundenlohn_glasreinigung: float
    stundenlohn_grundreinigung: float
    stundenlohn_sonderreinigung: float
    lohnzuschlag_prozent: float

class OverheadParameters(BaseModel):
    materialprozentsatz: float
    overhead_verwaltung_prozent: float
    ziel_gewinnmarge_prozent: float

class SurchargeParameters(BaseModel):
    regionalfaktor_nrw_prozent: float
    # Add other surcharges

class GeneralParameters(BaseModel):
    anfahrt_preis_pro_km: float
    mwst_prozent: float

class MasterData(BaseModel):
    unternehmen: CompanySettings
    lohnkosten: WageParameters
    material_overhead: OverheadParameters
    zuschlaege: SurchargeParameters
    sonstiges: GeneralParameters

# --- Service Catalog Models ---

class ServiceType(BaseModel):
    label: str
    leistungswert_m2_h: float
    leistungswert_min: float = 0.0
    leistungswert_max: float = 0.0
    basis_preis_m2_min: float = 0.0
    basis_preis_m2_max: float = 0.0
    beschreibung: str = ""
    raumgruppe: Optional[str] = None
    schwierigkeit: Optional[str] = None
    materialaufwand: Optional[str] = None
    zubehoer: Optional[List[str]] = []

class ServiceCategory(BaseModel):
    label: str
    icon: str
    beschreibung: str
    typen: Dict[str, ServiceType]

class ServiceCatalog(BaseModel):
    services: Dict[str, ServiceCategory]

# --- Calculation Models ---

class CalculationRequest(BaseModel):
    service_group_id: str # e.g. "unterhaltsreinigung"
    service_type_id: str # e.g. "buero_standard"
    area_sqm: float
    frequency_per_year: int = 1 # 1=yearly, 12=monthly, 52=weekly
    interval_factor: float = 1.0 # e.g. 52 weeks * X
    distance_km: float = 0.0
    difficulty_factor: float = 1.0 # 1.0 = Normal, 0.8 = Harder? No, factor usually multiplies time.
    # Let's say difficulty adjusts performance: adjusted_perf = base_perf * factor? 
    # Or factor multiplies price?
    # Standard: Difficulty reduces m²/h.
    
class CalculationResult(BaseModel):
    total_price_net: float
    total_price_gross: float
    price_per_sqm: float
    
    labor_costs: float
    material_costs: float
    overhead_costs: float
    profit_margin: float
    travel_costs: float
    
    hours_total: float
    hourly_rate_net: float # Calculated implicit rate
    
    breakdown: Dict[str, float] # Detailed cost breakdown

# --- JSON Data Models (for CalculationService) ---

class PriceRange(BaseModel):
    min: float
    max: float
    avg: float

class Addon(BaseModel):
    name: str
    price_factor: Optional[float] = None
    price_addition_per_sqm: Optional[float] = None

class CleaningType(BaseModel):
    id: str
    name: str
    category: str
    subcategory: Optional[str] = None
    description: str
    base_price_per_sqm: PriceRange
    performance_sqm_per_h: PriceRange
    addons: Optional[List[Addon]] = []

class CostParameters(BaseModel):
    wage_per_hour: float
    wage_overhead_factor: float
    material_markup_percent: float
    travel_cost_per_km: float
    overhead_percent: float
    target_margin_percent: float
    regional_factors: Dict[str, float]
    dirt_factors: Dict[str, float]
    setup_time_percent: float = 10.0 # Default 10% setup overhead

class CleaningData(BaseModel):
    cleaning_types: List[CleaningType]
    cost_parameters: CostParameters

