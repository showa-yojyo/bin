#!/usr/bin/env python
"""async08future.py: Use Future and ensure_future
cf. async09callback.py

Usage:
  async08future.py
"""
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def main():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    loop.run_until_complete(slow_operation(future))
    print(future.result())
    loop.close()

if __name__ == '__main__':
    main()
