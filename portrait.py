#!/usr/bin/env python

"""
Make landscape images portrait by using PIL (asyncio version)
"""

import asyncio
import sys
from PIL import Image


async def generate_images(queue, filenames):
    """Producer coroutine"""

    for filename in filenames:
        await queue.put(filename)

    print('All task requests sent')

async def rotate_images(queue):
    """Consumer coroutine"""

    while True:
        filename = await queue.get()
        print(f'Working on {filename}')
        try:
            image = Image.open(filename)
            if image.width <= image.height:
                # already portrait
                print(f'Skip {filename}')
                continue

            image_new = image.rotate(-90, expand=True)
            print(f'Saving {filename}')
            image_new.save(filename)
        finally:
            queue.task_done()

async def terminate_consumers(consumers):
    """Clean up consumers"""

    for consumer in consumers:
        consumer.cancel()

    await asyncio.gather(*consumers, return_exceptions=True)

async def main(filenames):
    """main entry point"""

    # Producer/consumer pattern
    queue = asyncio.Queue()

    # turn on the rotate_images thread
    consumers = [asyncio.create_task(rotate_images(queue)) for _ in range(3)]
    await generate_images(queue, filenames)

    # block until all tasks are done
    await queue.join()
    print('All work completed')

    await terminate_consumers(consumers)

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
