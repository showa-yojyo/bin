#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-task.html より

Features:
- asynio.get_running_loop()
- asynio.sleep()
- asyncio.run()
"""

import asyncio
import datetime

async def display_date():
    """Display the current date every second for 5 seconds
    """

    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break

        # Suspend the current task
        await asyncio.sleep(1)

asyncio.run(display_date())
