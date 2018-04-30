#!/usr/bin/env python
"""future05process.py: Use ProcessPoolExecutor.

Usage:
  future05process.py
"""

from concurrent.futures import ProcessPoolExecutor
from math import (floor, sqrt)

NUMBERS = (
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419,
    )

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(floor(sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with ProcessPoolExecutor() as executor:
        #result = executor.map(is_prime, NUMBERS, timeout=1)
        result = executor.map(is_prime, NUMBERS)
        for i, j in zip(NUMBERS, result):
            print(f'{i} is prime: {j}')

if __name__ == '__main__':
    main()
