#!/usr/bin/env python3
"""
    This Module contains a function to to_kv that returns a turple
"""
from typing import List, Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
        This function returns a tuple of a string and an int | float

        Argument:
            k: a string
            v: a float or int argument

        Return: A tuple of str and int | float.
    """
    new_tuple = (k, v ** 2)
    return new_tuple
