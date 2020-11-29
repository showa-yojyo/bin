#!/usr/bin/env python
"""mp6queue.py: Use multiprocessing.Queue (cf. mp4start.py)

Usage:
  mp6queue.py
"""
import multiprocessing as mp

def f(q):
    q.put([42, None, 'hello'])

def main():
    q = mp.Queue()
    p = mp.Process(target=f, args=(q,))
    p.start()
    print(q.get())
    p.join()

if __name__ == '__main__':
    main()
