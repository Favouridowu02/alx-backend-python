#!/usr/bin/env python3
"""
    This Module contains an annotated function
"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
        This is an Anotated function

        Argument:
            lst: an Iterable Sequence
        Return: a Tuple of Sequence and int
    """
    return [(i, len(i)) for i in lst]
