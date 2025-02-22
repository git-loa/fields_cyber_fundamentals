import unittest
from Exercise_for_2_1 import group_pow

class TestGroupPow(unittest.TestCase):
    def test_group_pow(self):
        self.assertEqual(group_pow(lambda x,y : x+y, 45, 34, 0), 1530)
        self.assertEqual(group_pow(lambda x,y : (x*y)% 67 , 45, 34, 1), 52)

if __name__ =="__main__":
    unittest.main()
