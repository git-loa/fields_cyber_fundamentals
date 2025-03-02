#!/usr/bin/python3
"""
Testing module
"""

import unittest
import CyberFoundations.exercise_package as ep
import Exercise_for_2_2 as ex22
from Exercise_for_2_1 import group_pow


# Exercise 1 functions
class TestExOneFuncs(unittest.TestCase):
    """
    Test functions in Exercise 1
    """

    def test_gcd(self):
        """
        Test function gcd
        """
        self.assertEqual(ep.gcd(48, 18), 6)
        self.assertEqual(ep.gcd(18, 48), 6)
        self.assertEqual(ep.gcd(12, 8), 4)
        self.assertEqual(ep.gcd(8, 12), 4)
        self.assertEqual(ep.gcd(12, 0), 12)
        self.assertEqual(ep.gcd(0, 12), 12)
        self.assertEqual(ep.gcd(0, 0), 0)
        self.assertEqual(ep.gcd(-12, 8), 4)
        self.assertEqual(ep.gcd(12, -8), 4)

    def test_bezout_coeffs(self):
        """
        Test the function bezout_coeffs
        """
        self.assertEqual(ep.bezout_coeffs(12, 8), (4, 1, -1))

    def test_extended_gcd(self):
        """
        Test the function extended_gcd
        """
        self.assertEqual(ep.extended_gcd(12, 8), (4, 1, -1))

    def test_break_rsa(self):
        """
        Test the function break_rsa
        """
        self.assertEqual(
            ep.break_rsa(948047, 2430101, 1223, 1473513), 1070777
        )  # Must pass
        self.assertEqual(
            ep.break_rsa(540950087, 1963323259, 40289, 1128982103), 401429893
        )  # Must pass
        self.assertEqual(
            ep.break_rsa(1151384497, 2017780463, 33191, 1154218329), 1792339949
        )  # Must pass

        # Must fail
        # self.assertEqual(break_rsa(1151384497, 2017780463, 33191, 1154218329), 179233994).


class TestExTwoFuncs(unittest.TestCase):
    """
    Class to test functions in Exercise 2
    """

    ring = ex22.Ring(lambda x, y: x + y, lambda x, y: x * y, 1, 0, lambda x: -x)
    field = ex22.Field(
        lambda x, y: x + y, lambda x, y: x * y, 1, 0, lambda x: -x, lambda x: 1 / x
    )
    field1 = ex22.Field(
        lambda x, y: (x + y) % 13,
        lambda x, y: (x * y) % 13,
        1,
        0,
        lambda x: -x,
        lambda x: ep.mod_inv(x, 13),
    )

    def test_group_pow(self):
        """
        Test the function group_pow
        """
        self.assertEqual(group_pow(lambda x, y: x + y, 45, 34, 0), 1530)
        self.assertEqual(group_pow(lambda x, y: (x * y) % 67, 45, 34, 1), 52)

    def test_polynomial_division(self):
        """
        Test the function polynomial_division
        """
        # q, r = field.polynomial_division([7,0,0,0,2,1], [-5,0,0,1])
        self.assertEqual(
            TestExTwoFuncs.field.polynomial_division([7, 0, 0, 0, 2, 1], [-5, 0, 0, 1]),
            ([0, 2.0, 1.0], [7.0, 10.0, 5.0]),
        )
        self.assertEqual(
            TestExTwoFuncs.field.polynomial_division([1, -3, 0, 2], [1, -1]),
            ([1.0, -2.0, -2.0], []),
        )

    def test_polynomial_addition(self):
        """
        Test the function polynomial_addition
        """
        self.assertEqual(TestExTwoFuncs.ring.polynomial_addition([1], [-1]), [])
        self.assertEqual(TestExTwoFuncs.ring.polynomial_addition([1], []), [1])
        self.assertEqual(TestExTwoFuncs.ring.polynomial_addition([1], [1]), [2])
        self.assertEqual(
            TestExTwoFuncs.ring.polynomial_addition([1, 2], [4, 5, 9]), [5, 7, 9]
        )

    def test_polynomial_mutiplication(self):
        """
        Test the function polynomial_mutiplication
        """
        self.assertEqual(
            TestExTwoFuncs.ring.polynomial_multiplication([4, 5, 9], [1, 2]),
            [4, 13, 19, 18],
        )
        self.assertEqual(TestExTwoFuncs.ring.polynomial_multiplication([1], [1]), [1])
        self.assertEqual(
            TestExTwoFuncs.ring.polynomial_multiplication([1, 2], [1]), [1, 2]
        )
        self.assertEqual(TestExTwoFuncs.ring.polynomial_multiplication([1, 2], []), [])

    def test_extended_euclidean(self):
        """
        Test the function extended_euclidean for polynomials
        """
        self.assertEqual(
            TestExTwoFuncs.field1.extended_euclidean(
                [-1, 0, 0, 0, 0, 1], [-3, 2, 0, 1]
            ),
            ([4, 9], [12, 4], [12, 8, 1, 9]),
        )


if __name__ == "__main__":
    unittest.main()
