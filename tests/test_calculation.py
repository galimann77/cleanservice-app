import unittest
import os
import sys
import os

# Add relevant paths
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from services.calculation import CalculationService
from models.data_models import CalculationRequest

class TestCalculationService(unittest.TestCase):
    def setUp(self):
        # Ensure we are loading the data correctly. 
        # In a real scenario, we might want to mock the data loading.
        self.service = CalculationService()

    def test_load_data(self):
        self.assertIsNotNone(self.service.data)
        self.assertGreater(len(self.service.data.cleaning_types), 0)

    def test_basic_calculation(self):
        # office cleaning
        req = CalculationRequest(
            cleaning_type_id="maintenance_office",
            area_sqm=100.0,
            region="Standard",
            dirt_level="normal",
            frequency="wöchentlich"
        )
        result = self.service.calculate_price(req)
        
        self.assertGreater(result.total_price_net, 0)
        self.assertGreater(result.estimated_hours, 0)
        
        # Check basic consistency
        # 100 sqm / 150 sqm/h (avg) = 0.66 hours
        # Price should be roughly around that.
        print(f"Basic Office Calc: {result.total_price_net} EUR ({result.estimated_hours}h)")

    def test_stone_cleaning_with_addons(self):
        # Stone cleaning with addons
        req = CalculationRequest(
            cleaning_type_id="stone_paving",
            area_sqm=50.0,
            region="NRW",
            dirt_level="stark",
            selected_addons=["Fugen reinigen", "Imprägnieren"]
        )
        result = self.service.calculate_price(req)
        
        print(f"Stone Cleaning Calc: {result.total_price_net} EUR ({result.estimated_hours}h)")
        
        # Verify dirt factor impact
        # Normal perfromance ~75 sqm/h. Stark = 1.3 factor -> ~57 sqm/h
        # 50 sqm / 57 sqm/h ~ 0.87h
        self.assertAlmostEqual(result.details['dirt_factor'], 1.3)
        self.assertGreater(result.estimated_hours, 0.5)

    def test_invalid_id(self):
        req = CalculationRequest(
            cleaning_type_id="invalid_id",
            area_sqm=100
        )
        with self.assertRaises(ValueError):
            self.service.calculate_price(req)

if __name__ == '__main__':
    unittest.main()
