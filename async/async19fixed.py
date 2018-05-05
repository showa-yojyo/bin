#!/usr/bin/env python
"""async19fixed.py: Chain coroutines (fixed)

Usage:
  async19fixed.py
"""

import asyncio

async def create():
    await asyncio.sleep(3.0)
    print("(1) create file")

async def write():
    await asyncio.sleep(1.0)
    print("(2) write into file")

async def close():
    print("(3) close file")

async def test(loop):
    await create() # == await asyncio.ensure_future(create())
    await write()
    await close()
    await asyncio.sleep(2.0)
    loop.stop()

def main():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(test(loop))
    loop.run_forever()
    print(f"Pending tasks at exit: {asyncio.Task.all_tasks(loop)}")
    loop.close()

if __name__ == '__main__':
    main()
