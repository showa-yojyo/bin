#!/usr/bin/env python
"""future04thread.py: Use ThreadPoolExecutor.

Usage:
  future04thread.py
"""
from concurrent.futures import (
    ThreadPoolExecutor, as_completed)
from urllib.request import urlopen

URLS = (
    'https://twitter.com/showa_yojyo',
    'http://www.geocities.jp/showa_yojyo/',
    'https://github.com/showa-yojyo',
    'https://gist.github.com/showa-yojyo',
    'https://showa-yojyo.github.io/',
    )

def load_url(url, timeout):
    with urlopen(url, timeout=timeout) as conn:
        return conn.read()

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        futures = {executor.submit(load_url, url, 60): url for url in URLS}
        #for i in as_completed(futures, timeout=2):
        for i in as_completed(futures):
            url = futures[i]
            try:
                data = i.result()
                print(f'{url} is {len(data)} bytes')
            except Exception as exc:
                print(f'{url} generated an exception {exc}')

if __name__ == '__main__':
    main()
