#!/usr/bin/env python
"""async18subproc.py: Use create_subprocess_exec
cf. async17subproc.py

Usage:
  async18subproc.py
"""

import asyncio.subprocess
import sys

async def get_date():
    code = 'import datetime; print(datetime.datetime.now())'

    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE)
    proc = await create

    # Read one line of output
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit
    await proc.wait()
    return line

def main():
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    date = loop.run_until_complete(get_date())
    print(f"Current date: {date}")
    loop.close()

if __name__ == '__main__':
    main()
