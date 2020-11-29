#!/usr/bin/env python
"""async01hello.py: Hello world
cf. async05hello.py

Usage:
  async01hello.py
"""
import asyncio

def hello_world(loop):
    print('Hello world')
    loop.stop()

def main():
    loop = asyncio.get_event_loop()

    # Schedule a call to hello_world()
    loop.call_soon(hello_world, loop)

    # Blocking call interrupted by loop.stop()
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
