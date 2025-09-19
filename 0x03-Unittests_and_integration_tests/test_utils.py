#!/usr/bin/env python3
"""Generic utilities for github org client.
"""
import unittest
import requests
from unittest.mock import patch, Mock
from utils import memoize
from utils import get_json
from utils import access_nested_map
from parameterized import parameterized
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map
  
class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the access_nested_map function.
    """
    
    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that the function returns the expected value for a simple path
        and with multiple paths.
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ["a"]),
        ({"a": 1}, ["a", "b"]),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that a KeyError is raised for invalid paths,
        and that the exception message matches the missing key.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # KeyError message should be the missing key (the last attempted key)
        self.assertEqual(str(cm.exception), repr(path[-1]))

if __name__ == "__main__":
    unittest.main()


def get_json(url: str) -> Dict:
    """Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()

class TestGetJson(unittest.TestCase):
#unit tests for utils.get_json
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
#test that get_json returns the expected payload and that requests.get is called exactly once  with the url
        mock_response = Mock()
        mock_response.json.return_value = test_payload          
        mock_get.return_value = mock_response
         #call function under test
        result = get_json(test_url)
         #assert the mocked get was called with the test_url
        mock_get.assert_called_once_with(test_url)
         #assert the returned value
        self.assertEqual(result, test_payload)
        
class TestMemoize(unittest.TestCase):
    
    def test_memoize(self):
#test that memoize cached the result of a method
        class TestClass:
            def a_method(self):
                return 42
            
            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()    
#patch a method to trace calls
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            #call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property
            
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)  
            #method should be called once (memoized)
            mock_method.assert_called_once()
            
if __name__ == "__main__":
    unittest.main()    

        
