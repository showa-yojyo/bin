#!/usr/bin/env python
"""async02time.py: Use call_soon and call_later
cf. async06time.py

Usage:
  async02time.py
"""

import asyncio
from datetime import datetime

def display_date(end_time, loop):
    print(f'{datetime.now():%T}')

    if loop.time() + 1.0 < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

def main():
    loop = asyncio.get_event_loop()

    # Schedule the first call to display_date()
    end_time = loop.time() + 5.0
    loop.call_soon(display_date, end_time, loop)

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
