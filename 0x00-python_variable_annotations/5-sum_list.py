#!/usr/bin/env python3
"""
    This Module contains a function sum_list
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
        This Function returns the sum of the float list values

        Arguments:
            input_list: a List of float

        Return: The sum of the list[Float]
    """
    sum = 0.0
    for i in range(0, len(input_list)):
        sum += input_list[i]

    return sum
