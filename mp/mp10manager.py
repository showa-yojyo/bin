#!/usr/bin/env python
"""mp10manager.py: Use multiprocessing.Manager.

Usage:
  mp10manager.py
"""
import multiprocessing as mp

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

def main():
    with mp.Manager() as mgr:
        d = mgr.dict()
        l = mgr.list(range(10))
        p = mp.Process(target=f, args=(d, l,))
        p.start()
        p.join()

        print(d, l)

if __name__ == '__main__':
    main()
