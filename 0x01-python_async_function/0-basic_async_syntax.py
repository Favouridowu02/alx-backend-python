#!/usr/bin/env python3
"""
    This Module contains an asynchronous coroutine.
    It is used to delay
"""
import asyncio
import random
import time
from typing import IO


async def wait_random(max_delay: int = 10) -> float:
    """
        This Function is an asynchronous function that takes in an
        integer argument with a default value of 10.

        Arguments:
            max_delay: the max value for the random be created from.
            using 0 as the minimum. It has a default value of 10

        Return: It returns the total time spent to load.
    """
    t = random.uniform(0, max_delay)
    initial = time.perf_counter()
    await asyncio.sleep(t)
    final = time.perf_counter() - initial
    return final
