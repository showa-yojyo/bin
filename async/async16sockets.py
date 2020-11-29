#!/usr/bin/env python
"""async16sockets.py: Use open_connection.
cf. async03reader.py and async13sockets.py

Usage:
  async16sockets.py
"""

import asyncio
from socket import socketpair

async def wait_for_data(loop):
    # Create a pair of connected sockets
    rsock, wsock = socketpair()

    # Register the open socket to wait for data
    reader, writer = await asyncio.open_connection(sock=rsock, loop=loop)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = await reader.read(100)

    # Got data, we are done: close the socket
    print("Received:", data.decode())
    writer.close()

    # Close the second socket
    wsock.close()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_data(loop))
    loop.close()

if __name__ == '__main__':
    main()
