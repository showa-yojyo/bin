#!/usr/bin/env python
"""future03dead.py: Cause a deadlock

Usage:
  future03dead.py
"""
from concurrent.futures import ThreadPoolExecutor

def main():
    def wait_on_future():
        future2 = executor.submit(pow, 5, 2)
        # This will never complete because there is only one worker thread and
        # it is executing this function.
        print(future2.result())

    executor = ThreadPoolExecutor(max_workers=1)
    future1 = executor.submit(wait_on_future)

if __name__ == '__main__':
    main()
