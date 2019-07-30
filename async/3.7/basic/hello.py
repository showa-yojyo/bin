#!/usr/bin/env python

"""https://docs.python.org/3.7/library/asyncio-task.html より

Features:
- asyncio.sleep()
- asyncio.run()

"""
import asyncio

async def main():
    print('hello')

    # コメント：sleep() は与えられた時間後に完了する
    # awaitable object であると考えるのが良い。
    #
    # Awaitable とは coroutines, Task, Future の総称と考えて良い。
    await asyncio.sleep(1)
    print('world')

# コメント：run() の呼び出しで良くなったようだ。
asyncio.run(main())
