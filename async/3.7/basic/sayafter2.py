#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-task.html より

Features:
- asyncio.create_task()
- asyncio.sleep()
- asyncio.run()

"""
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    """runs 1 second faster than sayafter.py
    """

    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    # コメント：for ループで書いても問題ない

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
