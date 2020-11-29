#!/usr/bin/env python
"""async07chain.py: Chain coroutines

Usage:
  async07chain.py
"""
import asyncio

async def compute(x, y):
    print(f"Compute {x} + {y} ...")
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print(f"{x} + {y} = {result}")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_sum(1, 2))
    loop.close()

if __name__ == '__main__':
    main()
