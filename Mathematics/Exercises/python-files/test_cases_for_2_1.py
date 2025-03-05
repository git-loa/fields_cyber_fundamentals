#!/usr/bin/python3
"""
Testing module for Exercise 2.1
"""
import unittest
from exercise_for_2_1 import group_pow


class TestExercise22(unittest.TestCase):
    """
    Test Cases for Exercise 2.1 functions
    """

    def test_group_pow(self):
        """
        Test group_pow
        """
        self.assertEqual(group_pow(lambda x, y: x + y, 45, 34, 0), 1530)
        self.assertEqual(group_pow(lambda x, y: (x * y) % 67, 45, 34, 1), 52)


if __name__ == "__main__":
    unittest.main()
