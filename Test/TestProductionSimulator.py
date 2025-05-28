import random
import unittest
import math

from impl.ProductionSimulator import ProductionSimulator


class TestProductionSimulator(unittest.TestCase):
    def setUp(self):
        # Fixed seed for reproducibility
        random.seed(0)
        self.product_names = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
        # Generate deterministic quantities and parameters
        quantities = ProductionSimulator.generate_random_quantities(self.product_names, min_qty=10, max_qty=10)
        params, overall_capacity = ProductionSimulator.generate_random_parameters(self.product_names)
        # Override random quantities to fixed value
        self.products_config = {
            name: {
                'quantity': quantities[name],
                'unit_time': params[name]['unit_time'],
                'daily_capacity': params[name]['daily_capacity']
            } for name in self.product_names
        }
        self.simulator = ProductionSimulator(self.products_config, overall_capacity)

    def test_generate_random_quantities(self):
        q = ProductionSimulator.generate_random_quantities(['X', 'Y'], min_qty=5, max_qty=5)
        self.assertEqual(q, {'X': 5, 'Y': 5})

    def test_generate_random_parameters(self):
        params, cap = ProductionSimulator.generate_random_parameters(['A'])
        self.assertIn('A', params)
        self.assertIsInstance(params['A']['unit_time'], float)
        self.assertIsInstance(params['A']['daily_capacity'], int)
        self.assertIsInstance(cap, int)

    def test_calculate_total_time_positive(self):
        hours, days = self.simulator.calculate_total_time()
        # Hours and days should be positive
        self.assertGreater(hours, 0)
        self.assertGreater(days, 0)

    def test_report_contains_sections(self):
        report = self.simulator.report()
        self.assertIn('Production Simulation Report', report)
        self.assertIn('Products configuration', report)
        self.assertIn('Total production time', report)

    def test_zero_overall_capacity(self):
        # If overall capacity is zero, days should be infinite
        products = {'P1': {'quantity': 10, 'unit_time': 1, 'daily_capacity': 100}}
        sim = ProductionSimulator(products, 0)
        hours, days = sim.calculate_total_time()
        self.assertEqual(hours, round(10 * 1 / 60, 2))
        self.assertTrue(math.isinf(days))

    def test_zero_quantity(self):
        # If quantity is zero, both hours and days should be zero
        products = {'P1': {'quantity': 0, 'unit_time': 1, 'daily_capacity': 100}}
        sim = ProductionSimulator(products, 1000)
        hours, days = sim.calculate_total_time()
        self.assertEqual(hours, 0.0)
        self.assertEqual(days, 0.0)

if __name__ == '__main__':
    unittest.main()
