#!/usr/bin/env python3
"""
    This Module contains async function called wait_n
"""
import asyncio
import random
import time
from typing import List


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
        This Function returns a list of all the wait random time spent
        for each async call

        Arguments:
            n: A number of times to create a specified delay.
            max_delay: The Maximum value range in creating to time
            for the suspence
        Return: return the list if all the delays(float values
    """
    new_list = []
    wait_random = __import__('0-basic_async_syntax').wait_random
    for _ in range(n):
        delay = await wait_random(max_delay)
        new_list.append(delay)
    return new_list
