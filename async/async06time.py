#!/usr/bin/env python
"""async06time.py: Replace call_soon and call_later with coroutines
cf. async02time.py

Usage:
  async06time.py
"""

import asyncio
from datetime import datetime

async def display_date(loop):
    end_time = loop.time() + 5.0

    while True:
        print(f'{datetime.now():%T}')
        if loop.time() + 1.0 >= end_time:
            break

        await asyncio.sleep(1)

def main():
    loop = asyncio.get_event_loop()

    # Blocking call which returns when the display_date() coroutine is done
    loop.run_until_complete(display_date(loop))
    loop.close()

if __name__ == '__main__':
    main()
