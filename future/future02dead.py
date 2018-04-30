#!/usr/bin/env python
"""future02dead.py: Cause a deadlock.

Usage:
  future02dead.py
"""

from concurrent.futures import ThreadPoolExecutor
from time import sleep

def main():
    def wait_on_a():
        sleep(5)
        print(future_a.result())

    def wait_on_b():
        sleep(5)
        print(future_b.result())

    executor = ThreadPoolExecutor(max_workers=2)
    future_a = executor.submit(wait_on_b)
    future_b = executor.submit(wait_on_a)

if __name__ == '__main__':
    main()
