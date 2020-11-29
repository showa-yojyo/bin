#!/usr/bin/env python
"""async14tcpserver.py: TCP Echo server protocol

Usage:
  async14tcpserver.py
"""

import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message} from {addr}")

    print(f"Send: {message}", flush=True)
    writer.write(data)
    await writer.drain()

    print("Close the client socket", flush=True)
    writer.close()

def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
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
