#!/usr/bin/env python
"""mp8lock.py: Use multiprocessing.Lock.

Usage:
  mp8lock.py
"""

import multiprocessing as mp

def f(lock, i):
    lock.acquire()
    try:
        print('hello world', i)
    finally:
        lock.release()

def main():
    lock = Lock()
    for i in range(10):
        Process(target=f, args=(lock, i)).start()

if __name__ == '__main__':
    main()
