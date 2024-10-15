#!/usr/bin/env python3
"""
    This module contains a function task_wait_random
"""
import asyncio
import time
import random

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
        This Function create a task from wait_random

        Argument:
            max_delay: the max delay that will be used in the max_random
            Function

        Return: a asyncio.Task
    """
    return asyncio.create_task(wait_random(max_delay))
