#!/usr/bin/env python
"""mp1pool.py: Use multiprocessing.Pool

Usage:
  mp1pool.py
"""
from multiprocessing import Pool

def f(x):
    return x**2

def main():
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))

# TODO:
if __name__ == '__main__':
    main()
