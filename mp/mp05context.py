#!/usr/bin/env python
"""mp5context.py: Use multiprocessing.get_context (cf. mp4start.py)

Usage:
  mp5context.py
"""
import multiprocessing as mp

def foo(q):
    q.put('hello')

def main():
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

if __name__ == '__main__':
    main()
