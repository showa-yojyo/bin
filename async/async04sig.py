#!/usr/bin/env python
"""async04sig.py: Use a signal handler (only for UNIX)

Usage:
  async04sig.py
"""

import asyncio
import functools
import os
import signal

def ask_exit(signame):
    print(f"got signal {signame}: exit")
    loop.stop()

def main():
    loop = asyncio.get_event_loop()

    print("Event loop running forever, press Ctrl+C to interrupt.")
    print(f"pid {os.getpid()}: send SIGINT or SIGTERM to exit.")

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame))

    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
