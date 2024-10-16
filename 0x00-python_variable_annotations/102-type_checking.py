#!/usr/bin/env python3
"""
    This Module contains an annotated function zoom_array
"""
from typing import List, Tuple, Any


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
        This is an annotated function
    """
    zoomed_in: List = [
        item for item in lst
    ]
    return zoomed_in


array: Tuple[Any, ...] = (12, 72, 91)
zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, int(3.0))
