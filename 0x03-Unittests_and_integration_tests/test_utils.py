#!/usr/bin/env python3
"""
    This Module contains the unittest test cases utils module
"""
from unittest import TestCase, mock
from utils import access_nested_map, get_json
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

    @parameterized.expand([
        param(nested_map={}, path=("a",)),
        param(nested_map={"a": 1}, path=("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
            This method is used to test the exception of the access_nested_map
            function
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(TestCase):
    """
        This Class contains the test cases for the function `get_json`
    """
    @parameterized.expand([
        param(test_url="http://example.com", test_payload={"payload": True}),
        param(test_url="http://holberton.io", test_payload={"payload": False}),
    ])
    @mock.patch('utils.get_json')
    def test_get_json(self, mocked_get_json, test_url, test_payload):
        """
            This Method is used to test the the get_jsom method for expected
            results
        """
        mocked_get_json.return_value = test_payload
        result = mocked_get_json(test_url)
        self.assertEqual(result, test_payload)
