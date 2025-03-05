#!/usr/bin/python3
"""
Testing module for Exercise 1.2
"""
import unittest
import exercise_for_1_2 as ex12


class TestEx12(unittest.TestCase):
    """
    Test Cases for Exercise 1.2 functions
    """

    def test_mod_inv(self):
        """
        Test the function mod_inv
        """
        self.assertEqual(
            ex12.mod_inv(21454362362356235, 34623572343523462537647),
            17327503250328260511719,
        )
        self.assertEqual(ex12.mod_inv(7, 24), 7)
        self.assertEqual(ex12.mod_inv(3, 5), 2)

    def test_mod_inv_no_inverse(self):
        """
        Test case where inverse does not exist.
        """
        with self.assertRaises(ValueError) as context:
            ex12.mod_inv(4, 8)
        self.assertEqual(
            str(context.exception),
            "Inverse does not exist because 4 and 8 are not coprimes (GCD = 4)",
        )
        with self.assertRaises(ValueError) as context:
            ex12.mod_inv(3, 9)
        self.assertEqual(
            str(context.exception),
            "Inverse does not exist because 3 and 9 are not coprimes (GCD = 3)",
        )

    def test_mod_pow(self):
        """
        Test the function mod_pow
        """
        self.assertEqual(ex12.mod_pow(3, 218, 1000), 489)
        self.assertEqual(ex12.mod_pow(17, 183, 256), 113)
        self.assertEqual(ex12.mod_pow(2, 477, 1000), 272)
        self.assertEqual(ex12.mod_pow(11, 507, 1237), 322)

    def test_mod_pow_2(self):
        """
        Test the function mod_pow
        """
        self.assertEqual(ex12.mod_pow_2(3, 218, 1000), 489)
        self.assertEqual(ex12.mod_pow_2(17, 183, 256), 113)
        self.assertEqual(ex12.mod_pow_2(2, 477, 1000), 272)
        self.assertEqual(ex12.mod_pow_2(11, 507, 1237), 322)

    def test_phi(self):
        """
        Test the function phi
        """
        self.assertEqual(ex12.phi(24), 8)
        self.assertEqual(ex12.phi(500), 200)
        self.assertEqual(ex12.phi(4567), 4566)
        self.assertEqual(ex12.phi(1987), 1986)

    def test_fast_phi(self):
        """
        Test the function fast_phi
        """
        self.assertEqual(ex12.fast_phi(24), 8)
        self.assertEqual(ex12.fast_phi(500), 200)
        self.assertEqual(ex12.fast_phi(4567), 4566)
        self.assertEqual(ex12.fast_phi(1987), 1986)


if __name__ == "__main__":
    unittest.main()
