#!/usr/bin/env python3
"""
    This Module contains the unittest test cases utils module
"""
from unittest import TestCase
from utils import access_nested_map
from parameterized import parameterized, param


class TestAccessNestedMap(TestCase):
    """
        This Class Contains the test cases for the function
        `access_nested_map`
    """
    @parameterized.expand([
        param(nested_map={'a': 1}, path=('a',), expected=1),
        param(nested_map={'a': {"b": 2}}, path=("a",), expected={"b": 2}),
        param(nested_map={"a": {"b": 2}}, path=("a", "b"), expected=2),
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
            This method is used to test the access_nested_map function
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
