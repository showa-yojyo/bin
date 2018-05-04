#!/usr/bin/env python
"""async03reader.py: Use a reader

Usage:
  async03reader.py
"""

import asyncio
from socket import socketpair

def main():
    # Create a pair of connected file descriptors
    rsock, wsock = socketpair()

    loop = asyncio.get_event_loop()

    def reader():
        data = rsock.recv(100)
        print("Received:", data.decode())
        # We are done: unregister the file descriptor
        loop.remove_reader(rsock)
        # Stop the event loop
        loop.stop()

    # Register the file descriptor for read event
    loop.add_reader(rsock, reader)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    loop.run_forever()

    # We are done, close sockets and the event loop
    rsock.close()
    wsock.close()
    loop.close()

if __name__ == '__main__':
    main()
