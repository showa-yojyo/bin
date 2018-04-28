#!/usr/bin/env python
"""mp9valuearray.py: Use multiprocessing.Value and multiprocessing.Array.

Usage:
  mp9valuearray.py
"""
import multiprocessing as mp

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

def main():
    num = mp.Value('d', 0.0)
    arr = mp.Array('i', range(10))

    p = mp.Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:]) # explicitly copy

if __name__ == '__main__':
    main()
