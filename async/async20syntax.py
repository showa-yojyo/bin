#!/usr/bin/env python
"""async20syntax.py: Use new syntax ``await for``
cf. async15httpheader.py

Usage:
  async20syntax.py
"""

import asyncio

async def http_get(domain):
    reader, writer = await asyncio.open_connection(domain, 80)

    writer.write(b'\r\n'.join([
        b'GET / HTTP/1.1',
        b'Host: %b' % domain.encode('utf-8'),
        b'Connection: close',
        b'', b''
    ]))

    async for line in reader:
        print(f'>>> {line.decode()}', end='')
    print()

    writer.close()

def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(http_get('example.com'))
    finally:
        loop.close()

if __name__ == '__main__':
    main()
