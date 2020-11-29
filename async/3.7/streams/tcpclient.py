#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-stream.html より

Features:
- asyncio.open_connection()
- asyncio.run()

Classes:
- asyncio.StreamReader
- asyncio.StreamWriter

Usage:
$ tcpserver.py &
$ tcpclient.py
$ kill ...
"""

import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!'))
