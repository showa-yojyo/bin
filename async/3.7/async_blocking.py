#!/usr/bin/env python

"""https://stackoverflow.com/questions/41063331/how-to-use-asyncio-with-existing-blocking-library
"""

import asyncio
import logging
import time

concurrent = 3
delay = 5

# PYTHONASYNCIODEBUG=1
logging.basicConfig(level=logging.DEBUG)

def blocking():
    """A blocking function
    """

    time.sleep(delay)
    logging.debug('completed')

async def main(executor=None):
    """How to call blocking functions concurrently
    """
    loop = asyncio.get_running_loop()

    # Run blocking tasks concurrently. asyncio.wait will
    # automatically wrap these in Tasks. If you want explicit access
    # to the tasks themselves, use asyncio.ensure_future, or add a
    # "done, pending = asyncio.wait..." assignment
    await asyncio.wait(
        [loop.run_in_executor(executor, blocking) for _ in range(concurrent)],
        return_when=asyncio.ALL_COMPLETED)

# PYTHONASYNCIODEBUG=1
asyncio.run(main(), debug=True)
