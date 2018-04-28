#!/usr/bin/env python
"""mp3process.py: Use multiprocessing.Process

Usage:
  mp3process.py
"""
from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

def main():
    info('main')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

if __name__ == '__main__':
    main()
