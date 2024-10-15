#!/usr/bin/env python3
"""
    This Module contains a function measure_time that is measures the
    total execution time
"""
import time
import asyncio
import random


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> int:
    """
        This function measures the execution time for 
        wait_n(n, max_delay)

        Arguments:
            n: The number of times 
            max_delay: The maximum delay integer

        Return: total_time / n 
    """
    initial = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    return (time.perf_counter() - initial) / n
