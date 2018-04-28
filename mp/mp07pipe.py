#!/usr/bin/env python
"""mp7pipe.py: Use multiprocessing.Pipe.

Usage:
  mp7pipe.py
"""

import multiprocessing as mp

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

def main():
    parent, child = mp.Pipe() # Pipe is a function
    p = mp.Process(target=f, args=(child,))
    p.start()
    print(parent.recv(child))
    p.end()

if __name__ == '__main__':
    main()
