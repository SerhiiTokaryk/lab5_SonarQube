import unittest
import math
from logic import lab1_logic as logic


class TestLab1Logic(unittest.TestCase):

    def test_gcd(self):
        self.assertEqual(logic.gcd(48, 18), 6)
        self.assertEqual(logic.gcd(101, 103), 1)
        self.assertEqual(logic.gcd(17, 0), 17)
        self.assertEqual(logic.gcd(1, 999), 1)

    def test_lcg_generator(self):

        result = logic.lcg_generator(0, 1, 1, 10, 5)
        self.assertEqual(result, [1, 2, 3, 4, 5])
        self.assertEqual(len(result), 5)

    def test_cesaro_test(self):
        self.assertEqual(logic.cesaro_test([5]), 0)

        bad_sequence = [2, 4, 6, 8]
        self.assertEqual(logic.cesaro_test(bad_sequence), 0)

        good_sequence = [2, 3, 4, 5]
        expected_pi = math.sqrt(6)
        self.assertAlmostEqual(logic.cesaro_test(good_sequence), expected_pi, places=5)

    def test_period(self):

        period = logic.find_period_floyd(0, 1, 1, 4)
        self.assertEqual(period, 4)


if __name__ == '__main__':
    unittest.main()