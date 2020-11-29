#!/usr/bin/env python
"""async09callback.py: Explicitly set callback
cf. async08future.py

Usage:
  async09callback.py
"""

import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def main():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation(future))

    def got_result(future):
        print(future.result())
        loop.stop()

    future.add_done_callback(got_result)
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
