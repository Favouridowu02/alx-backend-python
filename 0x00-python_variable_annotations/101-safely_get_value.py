#!/usr/bin/python3
"""
    This Module contains a type-annotated function like safely_get_value
"""
from typing import Union, Mapping, Any, TypeVar, TypeAlias

T = TypeVar('T')
D: TypeAlias = Union[T, None]
R: TypeAlias = Union[Any, T]


def safely_get_value(dct: Mapping, key: Any, default: D = None) -> R:
    """
        This is an annotated function that return

        Arguments:
            dct: an instance of Mapping
    """
    if key in dct:
        return dct[key]
    else:
        return default
