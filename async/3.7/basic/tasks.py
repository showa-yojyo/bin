#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-task.html より

Features:
- asyncio.create_task()
- asyncio.run()
"""

import asyncio

async def nested():
    return 42

async def main():
    """
    When a coroutine is wrapped into a Task with functions like
    asyncio.create_task(), the coroutine is automatically scheduled
    to run soon.
    """

    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
