from sqlalchemy.orm import Session
from models.master_data import ServiceType, ServiceCategory
from models.company_settings import CompanySettings
from models.project_data import CleaningTask, Room, Project
from core.init_db import init_default_company_settings

class CalculationEngine:
    """
    Professional Calculation Engine for Building Cleaning.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.settings = self.db.query(CompanySettings).first()
        if not self.settings:
            # Auto-Init if missing
            init_default_company_settings()
            self.settings = self.db.query(CompanySettings).first()
            if not self.settings:
                # Fallback in memory if DB fails
                self.settings = CompanySettings(
                    hourly_rate=25.0,
                    vat_rate=19.0,
                    profit_margin=15.0,
                    setup_time_percentage=10.0
                )

    def calculate_task(self, task: CleaningTask) -> CleaningTask:
        room = task.room
        service = task.service_type
        
        # 1. Norm Determination
        base_performance = service.performance_avg
        adjusted_performance = base_performance / task.difficulty_factor
        
        hours_per_service = room.area_sqm / adjusted_performance
        minutes_per_service = hours_per_service * 60
        
        # Monthly Hours
        hours_per_month = (hours_per_service * task.frequency_per_year) / 12
        
        # 2. Wage Determination
        wage = self.settings.hourly_rate # Simplified: Single rate
        
        # 3. Labor Cost
        # Defaults for missing fields in simplified model
        social_security_percent = 80.0
        material_percent = 5.0
        equipment_percent = 2.0
        overhead_percent = 18.0
        
        labor_overhead_factor = 1 + (social_security_percent / 100)
        full_labor_rate = wage * labor_overhead_factor
        
        labor_cost_monthly = hours_per_month * full_labor_rate
        
        # 4. Total Cost
        material_cost = labor_cost_monthly * (material_percent / 100)
        equipment_cost = labor_cost_monthly * (equipment_percent / 100)
        
        base_cost = labor_cost_monthly + material_cost + equipment_cost
        
        # General Overhead
        overhead_cost = base_cost * (overhead_percent / 100)
        
        total_self_cost = base_cost + overhead_cost
        
        # 5. Price Determination
        target_margin = self.settings.profit_margin / 100
        if target_margin >= 0.99: target_margin = 0.99
            
        net_price_monthly = total_self_cost / (1 - target_margin)
        
        # Update Task
        task.performance_used = adjusted_performance
        task.minutes_per_service = minutes_per_service
        task.hours_per_month = hours_per_month
        task.labor_cost_per_month = labor_cost_monthly
        task.price_net_monthly = net_price_monthly
        
        return task

    def calculate_project(self, project: Project) -> Project:
        total_net = 0.0
        total_hours = 0.0
        
        current_area = 0.0
        for room in project.rooms:
            current_area += room.area_sqm
            for task in room.tasks:
                self.calculate_task(task)
                total_net += task.price_net_monthly
                total_hours += task.hours_per_month
                
        # Apply Setup Time (Fix for setup logic in Engine)
        # Using simplified logic: Add % to total price or hours?
        # Usually setup is time. Let's add it to price for now as overhead.
        # But wait, self.settings.setup_time_percentage exists.
        # Let's add it to the Net Price as a separate position or surcharge?
        # User requirement: "Rüstzeiten (+10%)"
        
        setup_surcharge = total_net * (self.settings.setup_time_percentage / 100)
        total_net += setup_surcharge
        
        project.total_area = current_area
        project.total_price_net = total_net
        project.total_hours_monthly = total_hours
        
        return project

    def _get_wage_for_category(self, category_id: str) -> float:
        return self.settings.hourly_rate
