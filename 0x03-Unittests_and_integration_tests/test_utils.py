#!/usr/bin/env python3
"""Generic utilities for github org client.
"""
import unittest
import requests
from utils import acces_nested_map
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

if __name__ == "__main__":
    unittest.main()
  
