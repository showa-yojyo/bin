#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-task.html 変奏版

Features:
- asyncio.gather()
- asyncio.sleep()
- asyncio.run()
"""

import asyncio
import logging
import time

concurrent = 3
delay = 5

# PYTHONASYNCIODEBUG=1
logging.basicConfig(level=logging.DEBUG)

async def async_pause():
    await asyncio.sleep(delay)
    return 0

async def sync_pause():
    time.sleep(delay)
    return 0

async def main():
    """Schedule three calls *concurrently*"""

    tasks = [
        async_pause() for _ in range(concurrent)]
    await asyncio.gather(*tasks)

    tasks =[
        sync_pause() for _ in range(concurrent)]
    await asyncio.gather(*tasks)

# PYTHONASYNCIODEBUG=1
asyncio.run(main(), debug=True)
