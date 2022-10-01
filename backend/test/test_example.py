import unittest
from app.example_code import calc_add


class TestAddMethod(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(calc_add(1, 1), 2)

    def test_negitive(self):
        self.assertEqual(calc_add(-1, -1), -2)


if __name__ == '__main__':
    unittest.main()
