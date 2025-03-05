#!/usr/bin/python3
"""
Testing module for Exercise 1.4
"""

import unittest
import exercise_for_1_4 as ex14
import CyberFoundations.exercise_package as ep


class TestEx14(unittest.TestCase):
    """
    Test Exerise 1.4 functions
    """

    def test_is_prime(self):
        """
        Test is_prime
        """
        self.assertEqual(ex14.is_prime(1105)[0], False)
        self.assertEqual(ex14.is_prime(294409)[0], False)
        self.assertEqual(ex14.is_prime(294439)[0], True)
        self.assertEqual(ex14.is_prime(118901509)[0], True)
        self.assertEqual(ex14.is_prime(118901521)[0], False)
        self.assertEqual(ex14.is_prime(118901527)[0], True)
        self.assertEqual(ex14.is_prime(118915387)[0], False)
        self.assertEqual(ex14.is_prime(1987)[0], True)
        self.assertEqual(ex14.is_prime(1993)[0], True)

    def test_get_prime(self):
        """
        Test get_prime
        """
        self.assertEqual(ex14.is_prime(ex14.get_prime(100))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_prime(101))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_prime(102))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_prime(103))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_prime(104))[0], True)

    def test_get_safe_prime(self):
        """
        Test get_safe_prime
        """
        self.assertEqual(ex14.is_prime(ex14.get_safe_prime(100))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_safe_prime(101))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_safe_prime(102))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_safe_prime(103))[0], True)
        self.assertEqual(ex14.is_prime(ex14.get_safe_prime(104))[0], True)

    def test_get_primitive_root(self):
        """
        Test get_primitive_root
        """
        self.assertEqual(
            ep.is_primitive(
                ex14.get_primitive_root(1324631307432395802967872697157),
                1324631307432395802967872697157,
            ),
            True,
        )


if __name__ == "__main__":
    unittest.main()
