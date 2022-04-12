import unittest

from app import get_numbers


class TestGetNumbers(unittest.TestCase):
    def test_multiplication(self):
        self.assertEqual(get_numbers(10, 2, '*'), 20)
