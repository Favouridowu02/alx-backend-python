#!/usr/bin/env python3
"""
    This Module contains an asynchronous coroutine.
    It is used to delay
"""
import asyncio
import random
import time

async def wait_random(max_delay=10):
    """
        This Function is an asynchronous function that takes in an
        integer argument with a default value of 10.

        Arguments:
            max_delay: the max value for the random be created from.
            using 0 as the minimum. It has a default value of 10

        Return: It returns the total time spent to load.
    """
    t = random.randint(0, max_delay)
    initial = time.time()
    await asyncio.sleep(t)
    time_difference = time.time() - 1
    return time_difference


