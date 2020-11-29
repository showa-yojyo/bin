#!/usr/bin/env python
"""async12udpserver.py: UDP Echo server protocol

Usage:
  async12udpserver.py
"""

import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print(f'Received {message!r} from {addr}')
        print(f'Send {message!r} to {addr}', flush=True)
        self.transport.sendto(data, addr)

def main():
    loop = asyncio.get_event_loop()
    print("Starting UDP server", flush=True)
    # One protocol instance will be created to serve all client requests
    listen = loop.create_datagram_endpoint(
        EchoServerProtocol, local_addr=('127.0.0.1', 9999))
    transport, protocol = loop.run_until_complete(listen)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()

if __name__ == '__main__':
    main()
