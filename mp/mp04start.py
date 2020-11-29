#!/usr/bin/env python
"""mp4start.py: Use multiprocessing.set_start_method

Usage:
  mp4start.py
"""
import multiprocessing as mp

def foo(q):
    q.put('hello')

def main():
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

if __name__ == '__main__':
    main()
