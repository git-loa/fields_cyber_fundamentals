#!/usr/bin/python3

"""
Testing module for Exercise 2.2
"""
import unittest
import CyberFoundations.exercise_package as ep
import exercise_for_2_2 as ex22


class TestEx22(unittest.TestCase):
    """
    Test Cases for Exercise 2.2 functions
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

    def test_reduce(self):
        """
        Test reduce
        """
        self.assertEqual(
            TestEx22.ring.reduce([2, 3, 4, 0, 5, 0, 0, 0, 0]), [2, 3, 4, 0, 5]
        )

    def test_degree(self):
        """
        Test degree
        """
        self.assertEqual(TestEx22.ring.degree([]), 0)
        self.assertEqual(TestEx22.ring.degree([1]), 0)
        self.assertEqual(TestEx22.ring.degree([0, 1]), 1)
        self.assertEqual(TestEx22.ring.degree([1, 0, 1]), 2)

    def test_polynomial_division(self):
        """
        Test the function polynomial_division
        """
        self.assertEqual(
            TestEx22.field.polynomial_division([7, 0, 0, 0, 2, 1], [-5, 0, 0, 1]),
            ([0, 2.0, 1.0], [7.0, 10.0, 5.0]),
        )
        self.assertEqual(
            TestEx22.field.polynomial_division([1, -3, 0, 2], [1, -1]),
            ([1.0, -2.0, -2.0], []),
        )

    def test_polynomial_mutiplication(self):
        """
        Test the function polynomial_mutiplication
        """
        self.assertEqual(
            TestEx22.ring.polynomial_multiplication([4, 5, 9], [1, 2]),
            [4, 13, 19, 18],
        )
        self.assertEqual(TestEx22.ring.polynomial_multiplication([1], [1]), [1])
        self.assertEqual(TestEx22.ring.polynomial_multiplication([1, 2], [1]), [1, 2])
        self.assertEqual(TestEx22.ring.polynomial_multiplication([1, 2], []), [])

    def test_polynomial_addition(self):
        """
        Test the function polynomial_addition
        """
        self.assertEqual(TestEx22.ring.polynomial_addition([1], [-1]), [])
        self.assertEqual(TestEx22.ring.polynomial_addition([1], []), [1])
        self.assertEqual(TestEx22.ring.polynomial_addition([1], [1]), [2])
        self.assertEqual(
            TestEx22.ring.polynomial_addition([1, 2], [4, 5, 9]), [5, 7, 9]
        )

    def test_scalar_multiply(self):
        """
        Test scalar multiplication
        """
        self.assertEqual(TestEx22.ring.scalar_multiply([1, 2, 3], 2), [2, 4, 6])
        self.assertEqual(TestEx22.ring.scalar_multiply([1, 2, 3], -2), [-2, -4, -6])

    def test_extended_euclidean(self):
        """
        Test the function extended_euclidean for polynomials
        """
        self.assertEqual(
            TestEx22.field1.extended_euclidean([-1, 0, 0, 0, 0, 1], [-3, 2, 0, 1]),
            ([4, 9], [12, 4], [12, 8, 1, 9]),
        )

    def test_byte_to_poly(self):
        """
        Test byte_to_poly
        """
        self.assertEqual(ex22.byte_to_poly(83), [1, 1, 0, 0, 1, 0, 1])

    def test_poly_to_byte(self):
        """
        Test poly_to_byte
        """
        self.assertEqual(ex22.poly_to_byte([1, 1, 0, 0, 1, 0, 1]), 83)

    def test_make_aes_mult_table(self):
        """
        Test make_aes_mult_table
        """
        aes_mult = ex22.make_aes_mult_table()
        self.assertEqual(aes_mult[83][202], 1)


if __name__ == "__main__":
    unittest.main()
