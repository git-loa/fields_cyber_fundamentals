#!/usr/bin/python3

"""
Testing module for Exercise 1.1
"""

import unittest
import exercise_for_1_1 as ex11


class TestEx11(unittest.TestCase):
    """
    Test Exercise 1.1 functions
    """

    def test_gcd(self):
        """
        Test function gcd
        """
        self.assertEqual(ex11.gcd(48, 18), 6)
        self.assertEqual(ex11.gcd(18, 48), 6)
        self.assertEqual(ex11.gcd(12, 8), 4)
        self.assertEqual(ex11.gcd(8, 12), 4)
        self.assertEqual(ex11.gcd(12, 0), 12)
        self.assertEqual(ex11.gcd(0, 12), 12)
        self.assertEqual(ex11.gcd(0, 0), 0)
        self.assertEqual(ex11.gcd(-12, 8), 4)
        self.assertEqual(ex11.gcd(12, -8), 4)

    def test_bezout_coeffs(self):
        """
        Test the function bezout_coeffs
        """
        self.assertEqual(ex11.bezout_coeffs(12, 8), (4, 1, -1))

    def test_extended_gcd(self):
        """
        Test the function extended_gcd
        """
        self.assertEqual(ex11.extended_gcd(12, 8), (4, 1, -1))


if __name__ == "__main__":
    unittest.main()
