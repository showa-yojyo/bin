#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-task.html より

Features:
- asyncio.gather()
- asyncio.sleep()
- asyncio.run()
"""

import asyncio

async def factorial(name, number):
    """Return $n!$
    """

    # コメント：最適化がなされていないのは意図的だ

    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4))

asyncio.run(main())
