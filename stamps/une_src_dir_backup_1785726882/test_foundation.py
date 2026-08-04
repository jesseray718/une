"""Unit tests for UNE Foundation Calculator and Core Equations."""
import unittest
from une.foundation_calc import (
    labor_intensity, efficiency_ratio, time_to_place,
    person_hours, compare_systems, truck_limited_rate,
)
from une.core_equations import efficiency, substitution_valid, composition_beneficial

class TestFoundationCalc(unittest.TestCase):
    def test_labor_intensity(self):
        self.assertAlmostEqual(labor_intensity(40, 55), 40/55)
        self.assertEqual(labor_intensity(0, 55), 0.0)
        self.assertEqual(labor_intensity(10, 0), float("inf"))

    def test_efficiency_ratio(self):
        self.assertAlmostEqual(efficiency_ratio(0.727, 0.0218), 0.727/0.0218, places=1)
        self.assertEqual(efficiency_ratio(10, 0), float("inf"))

    def test_time_to_place(self):
        self.assertAlmostEqual(time_to_place(55, 46), 55/46)
        self.assertEqual(time_to_place(55, 0), float("inf"))

    def test_person_hours(self):
        self.assertEqual(person_hours(5, 8), 40)
        self.assertEqual(person_hours(1, 1.2), 1.2)

    def test_truck_limited_rate(self):
        rate = truck_limited_rate(7.65, 10)
        self.assertAlmostEqual(rate, 45.9, places=1)

    def test_compare_systems(self):
        result = compare_systems("Trad", 5, 8, 55, "Pump", 1, 1.2, 55)
        self.assertAlmostEqual(result["ratio_labor_efficiency_B_vs_A"], 33.3, places=0)

class TestCoreEquations(unittest.TestCase):
    def test_efficiency(self):
        self.assertEqual(efficiency(100, 20), 5.0)
        self.assertEqual(efficiency(100, 0), float("inf"))
        self.assertEqual(efficiency(0, 0), 0.0)

    def test_substitution_valid(self):
        self.assertTrue(substitution_valid(100, 20, 30, 50, 50))
        self.assertFalse(substitution_valid(100, 80, 30, 50, 50))
        self.assertFalse(substitution_valid(100, 20, 30, 50, 40))

    def test_composition_beneficial(self):
        self.assertTrue(composition_beneficial(2.0, 3.0, 4.0))
        self.assertFalse(composition_beneficial(2.0, 3.0, 2.5))

if __name__ == "__main__":
    unittest.main(verbosity=2)
