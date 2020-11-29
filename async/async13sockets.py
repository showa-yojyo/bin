#!/usr/bin/env python
"""async13sockets.py: Use create_connection
cf. async03reader.py and async16sockets.py

Usage:
  async13sockets.py
"""
import asyncio
from socket import socketpair

class MyProtocol(asyncio.Protocol):
    transport = None

    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Received:", data.decode())

        # We are done: close the transport (it will call connection_lost())
        self.transport.close()

    def connection_lost(self, exc):
        # The socket has been closed, stop the event loop
        self.loop.stop()

def main():
    # Create a pair of connected sockets
    rsock, wsock = socketpair()
    loop = asyncio.get_event_loop()

    # Register the socket to wait for data
    connect_coro = loop.create_connection(
        lambda: MyProtocol(loop),
        sock=rsock)
    transport, protocol = loop.run_until_complete(connect_coro)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Run the event loop
    loop.run_forever()

    # We are done, close sockets and the event loop
    rsock.close()
    wsock.close()
    loop.close()

if __name__ == '__main__':
    main()
