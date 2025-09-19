#!/usr/bin/env python3
"""Generic utilities for github org client.
"""
import requests
import unitest
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

  @parameterized.expand([
       ({"a": 1}, ["a"], 1),
       ({"a": {"b": 2}}, ["a"], {"b": 2}),
       ({"a": {"b": 2}}, ["a", "b"], 2), 
  ])
  def test_access_nested_map_with_parameters(self, nested_map, path, expected) :
    #test that correct values are returned
      result = access_nested_map(nested_map, path)
      self.assertEqual(access_nested_map(nested_path), expected) 
      
if __name__ == __"main"__:
    unitest.main()
  
