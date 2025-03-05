#!/usr/bin/python3
"""
Testing module Exercise 1.5
"""

import unittest
import exercise_for_1_5 as ex15
import CyberFoundations.exercise_package as ep


class TestEx15(unittest.TestCase):
    """
    Test function in Exercise 1.5
    """

    def test_chinese_remainder(self):
        """
        Test chinese_remainder
        """
        self.assertEqual(
            ex15.chinese_remainder(
                [7, 9],
                [3, 4],
            ),
            31,
        )
        self.assertEqual(
            ex15.chinese_remainder(
                [423, 191],
                [137, 87],
            ),
            27209,
        )
        self.assertEqual(
            ex15.chinese_remainder(
                [9, 10, 11],
                [5, 6, 7],
            ),
            986,
        )

        self.assertEqual(
            ex15.chinese_remainder(
                [43, 49, 71],
                [37, 22, 18],
            ),
            11733,
        )

        self.assertEqual(
            ex15.chinese_remainder(
                [5, 11, 17],
                [2, 3, 5],
            ),
            872,
        )

    def test_chinese_remainder_no_solution(self):
        """
        Test case where list of moduli are not pairwise coprimes
        """
        with self.assertRaises(ep.CoprimesError) as context:
            ex15.chinese_remainder(
                [451, 697],
                [133, 237],
            )
        self.assertEqual(
            str(context.exception),
            "The integers in [451, 697] are not pairwise coprimes.",
        )

        with self.assertRaises(ep.CoprimesError) as context:
            ex15.chinese_remainder(
                [2, 4, 6, 8],
                [1, 2, 3, 4],
            )
        self.assertEqual(
            str(context.exception),
            "The integers in [2, 4, 6, 8] are not pairwise coprimes.",
        )

        with self.assertRaises(ep.CoprimesError) as context:
            ex15.chinese_remainder(
                [2, 4, 5, 6, 8],
                [1, 2, 3, 4, 5],
            )
        self.assertEqual(
            str(context.exception),
            "The integers in [2, 4, 5, 6, 8] are not pairwise coprimes.",
        )


if __name__ == "__main__":
    unittest.main()
