#!/usr/bin/env python
"""async05hello.py: Hello world (coroutine version)
cf. async01hello.py

Usage:
  async05hello.py
"""
import asyncio

async def hello_world():
    print('Hello world')

def main():
    loop = asyncio.get_event_loop()

    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete(hello_world())
    loop.close()

if __name__ == '__main__':
    main()
