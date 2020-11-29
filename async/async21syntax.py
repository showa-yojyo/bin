#!/usr/bin/env python
"""async21syntax.py: Use new syntax ``await with``

Usage:
  async21syntax.py
"""

import asyncio

async def coro(name, lock):
    print(f'coro {name}: waiting for lock')
    async with lock:
        print(f'coro {name}: holding the lock')
        await asyncio.sleep(1)
        print(f'coro {name}: releasing the lock')

def main():
    loop = asyncio.get_event_loop()
    lock = asyncio.Lock()
    coros = asyncio.gather(
        coro(1, lock),
        coro(2, lock))
    try:
        loop.run_until_complete(coros)
    finally:
        loop.close()
    
if __name__ == '__main__':
    main()
