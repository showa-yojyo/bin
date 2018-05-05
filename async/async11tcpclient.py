#!/usr/bin/env python
"""async11tcpclient.py: TCP Echo client protocol

Assume that sync11tcpserver.py is running in another console.

Usage:
  async11tcpclient.py
"""

import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print(f'Data sent: {self.message!r}')

    def data_received(self, data):
        print(f'Data received: {data.decode()!r}')

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

def main():
    loop = asyncio.get_event_loop()
    message = 'Hello World!'
    coro = loop.create_connection(
        lambda: EchoClientProtocol(message, loop),
        '127.0.0.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
