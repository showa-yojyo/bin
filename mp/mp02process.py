#!/usr/bin/env python
"""mp2process.py: Use multiprocessing.Process

Usage:
  mp2process.py
"""
from multiprocessing import Process

def f(name):
    print('hello', name)

def main():
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

if __name__ == '__main__':
    main()
