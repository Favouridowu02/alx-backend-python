#!/usr/bin/env python3
"""
    This Module contains an anotated function
"""
from typing import List, Union, Sequence, Any, NewType

NoneType = NewType('NoneType', None)


def safe_first_element(lst: Sequence[Any]) -> Union[Any, NoneType]:
    """
        This is an annotated Function
    """
    if lst:
        return lst[0]
    else:
        return None
