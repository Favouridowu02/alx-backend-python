#!/usr/bin/env python3
"""
    This Module contains a type-annotated function make_multiplier
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
        This function  that takes a float multiplier as argument
        and returns a function that multiplies a float by multiplies
        a float by multiplier

        Arguments:
            multiplier: a float

        Return: Callable on a square of the multiplier
    """
    def fun(new: float):
        return new * multiplier

    return fun
