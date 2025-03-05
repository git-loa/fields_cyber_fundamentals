#!/usr/bin/python3
"""
Testing module Exercise 1.6
"""
import unittest
from exercise_for_1_6 import break_rsa


class TestBreakRsa(unittest.TestCase):
    """
    Test Exercise 1.6 functions
    """

    def test_break_rsa(self):
        """
        Test break_rsa
        """
        self.assertEqual(
            break_rsa(948047, 2430101, 1223, 1473513), 1070777
        )  # Must pass
        self.assertEqual(
            break_rsa(540950087, 1963323259, 40289, 1128982103), 401429893
        )  # Must pass
        self.assertEqual(
            break_rsa(1151384497, 2017780463, 33191, 1154218329), 1792339949
        )  # Must pass
        self.assertFalse(
            break_rsa(1151384497, 2017780463, 33191, 1154218329) == 179233994, False
        )


if __name__ == "__main__":
    print("\n ----------------- Optional  Exercice 1 ---------------- \n")
    print("Using Unittest to test break_rsa().")
    unittest.main()
