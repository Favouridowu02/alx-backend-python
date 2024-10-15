#!/usr/bin/env python3
"""
    This Module contains a function task_wait_n. That accepts
"""
import asyncio
import random
import time


async def task_wait_n(n, max_delay):
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
    task_wait_random = __import__('3-tasks').task_wait_random
    for _ in range(n):
        delay = await task_wait_random(max_delay)
        new_list.append(delay)
    return new_list
