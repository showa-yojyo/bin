#!/usr/bin/env python
"""future01with.py: Use ThreadPoolExecutor.submit.

Before run this script do:
    seq -f src%g.txt 4 | xargs touch

Usage:
  future01with.py
"""

from concurrent.futures import ThreadPoolExecutor
from shutil import copy

def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(copy, 'src1.txt', 'dest1.txt')
        executor.submit(copy, 'src2.txt', 'dest2.txt')
        executor.submit(copy, 'src3.txt', 'dest3.txt')
        executor.submit(copy, 'src4.txt', 'dest4.txt')

if __name__ == '__main__':
    main()
