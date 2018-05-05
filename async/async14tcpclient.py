#!/usr/bin/env python
"""async14tcpclient.py: TCP Echo client protocol

Assume that sync14tcpserver.py is running in another console.

Usage:
  async14tcpclient.py
"""

import asyncio

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888,
        loop=loop)

    print(f'Send: {message}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    print('Close the socket')
    writer.close()

def main():
    loop = asyncio.get_event_loop()
    message = 'Hello World!'
    loop.run_until_complete(tcp_echo_client(message, loop))
    loop.close()

if __name__ == '__main__':
    main()
