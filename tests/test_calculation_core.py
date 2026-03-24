import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base
from models.master_data import CompanySettings, ServiceType, ServiceCategory
from models.project_data import Project, Room, CleaningTask
from services.calculation_engine import CalculationEngine

class TestCalculationEngine(unittest.TestCase):
    
    def setUp(self):
        # In-memory DB for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()
        
        # Seed Master Data
        self.settings = CompanySettings(
            wage_maintenance=18.00,
            social_security_percent=80.0, # Factor 1.8
            material_percent=5.0,
            equipment_percent=2.0,
            overhead_percent=15.0,
            profit_margin_percent=20.0 # Price = Cost / 0.8
        )
        self.db.add(self.settings)
        
        # Seed Service
        self.cat = ServiceCategory(id="maintenance", name="Unterhalt")
        self.db.add(self.cat)
        self.srv = ServiceType(id="office", category_id="maintenance", name="Büro", performance_avg=200)
        self.db.add(self.srv)
        self.db.commit()
        
        self.engine_svc = CalculationEngine(self.db)

    def tearDown(self):
        self.db.close()

    def test_single_task_calculation(self):
        # Setup Project/Room/Task
        proj = Project(name="Test Project")
        room = Room(name="Office 1", area_sqm=100.0, room_type="office")
        task = CleaningTask(
            service_type_id="office",
            frequency_per_year=12, # Monthly
            difficulty_factor=1.0
        )
        room.tasks.append(task)
        proj.rooms.append(room)
        
        self.db.add(proj)
        self.db.commit()
        
        # Calculate
        calc_task = self.engine_svc.calculate_task(task)
        
        # Verify
        # 1. Time: 100m² / 200m²/h = 0.5 hours per service
        # Monthly Hours: 0.5 * 12 / 12 = 0.5 hours/month
        self.assertAlmostEqual(calc_task.hours_per_month, 0.5)
        
        # 2. Labor Cost: 0.5h * 18.00 * 1.8 = 0.5 * 32.4 = 16.20
        self.assertAlmostEqual(calc_task.labor_cost_per_month, 16.20)
        
        # 3. Total Cost
        # Base: 16.20 + (16.20*0.05) + (16.20*0.02) = 16.20 + 0.81 + 0.324 = 17.334
        # Overnight: 17.334 * (1 + 0.15) = 17.334 * 1.15 = 19.9341
        
        # 4. Price
        # Price = 19.9341 / (1 - 0.20) = 19.9341 / 0.8 = 24.9176
        
        self.assertAlmostEqual(calc_task.price_net_monthly, 24.917625, places=4)

if __name__ == "__main__":
    unittest.main()
