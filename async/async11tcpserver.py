#!/usr/bin/env python
"""async11tcpserver.py: TCP Echo server protocol

Usage:
  async11tcpserver.py
"""
import asyncio

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'Connection from {peername}', flush=True)
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print(f'Data received: {message!r}')

        print(f'Send: {message!r}')
        self.transport.write(data)

        print('Close the client socket', flush=True)
        self.transport.close()

def main():
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(EchoServerProtocol, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print(f'Serving on {server.sockets[0].getsockname()}', flush=True)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
