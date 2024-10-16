#!/usr/bin/env python3
"""
    This Model contains a function sum_mixed_list that accepts a
    list of float and int
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
        This function that accepts a list of int and float

        Arguments:
            mxd_list: a list of integers and Float

        Return: This returns a sum of the list values in float
    """
    sum = 0.0
    for i in range(0, len(mxd_lst)):
        sum += mxd_lst[i]
    return sum
