import unittest
import pytest

from app import get_numbers


# class TestGetNumbers(unittest.TestCase):
#     def test_multiplication(self):
#         self.assertEqual(get_numbers(10, 2, '*'), 20)

def test_get_numbers():
    assert get_numbers(10, 2, '*') == 20


def test_double():
    assert get_numbers(11, 2, '*') == 22
