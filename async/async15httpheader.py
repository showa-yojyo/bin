#!/usr/bin/env python
"""async15httpheader.py: Get HTTP header

Usage:
  async15httpheader.py http://example.com/path/page.html
"""

import asyncio
import urllib.parse
import sys

async def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        connect = asyncio.open_connection(url.hostname, 443, ssl=True)
    else:
        connect = asyncio.open_connection(url.hostname, 80)
    reader, writer = await connect
    path = url.path or '/'
    query = (f'HEAD {path} HTTP/1.0\r\n'
             'Host: {url.hostname}\r\n'
             '\r\n')
    writer.write(query.encode('utf-8'))
    while True:
        line = await reader.readline()
        if not line:
            break
        line = line.decode('utf-8').rstrip()
        if line:
            print(f'HTTP header> {line}')

    # Ignore the body, close the socket
    writer.close()

def main(url):
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(print_http_headers(url))
    try:
        loop.run_until_complete(task)
    finally:
        loop.close()

if __name__ == '__main__':
    main(sys.argv[1])
