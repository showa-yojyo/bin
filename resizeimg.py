#!/usr/bin/env python

import asyncio
import math
import sys
from PIL import Image

SCREEN_SIZE_PORTRAIT = (768, 1366)

def round_aspect(number, key):
    return max(min(math.floor(number), math.ceil(number), key=key), 1)


def desired_size(width, height):
    if width < height:
        x, y = SCREEN_SIZE_PORTRAIT
    else:
        y, x = SCREEN_SIZE_PORTRAIT

    # preserve aspect ratio
    aspect = width / height
    if x / y >= aspect:
        x = round_aspect(y * aspect, key=lambda n: abs(aspect - n / y))
    else:
        y = round_aspect(x / aspect, key=lambda n: abs(aspect - x / n))
    return (x, y)

async def generate_images(queue, filenames):
    """Producer coroutine"""

    for name in filenames:
        #print(f'Producing {name}')
        await queue.put((name, Image.open(name)))


def process_image(image):
    width_old, height_old = image.width, image.height
    size_new = desired_size(width_old, height_old)

    use_resize = False
    if width_old > height_old:
        # case of landscape
        use_resize = width_old < SCREEN_SIZE_PORTRAIT[1]
    else:
        # case of portrait
        use_resize = height_old < SCREEN_SIZE_PORTRAIT[1]

    if use_resize:
        image = image.resize(size_new, resample=Image.LANCZOS)
    else:
        image.thumbnail(size_new, resample=Image.LANCZOS)

    return image

async def process_images(queue):
    """Consumer coroutine"""

    while True:
        filename, image = await queue.get()
        try:
            image_new = process_image(image)
            if not image_new:
                print(f'Skip {filename} {image.size}')
                continue

            print(f'Saving {filename} {image_new.size}')
            image_new.save(filename)
        finally:
            queue.task_done()

async def main(filenames):
    """main entry point"""

    # Producer/consumer pattern
    queue = asyncio.Queue()

    consumers = [asyncio.create_task(process_images(queue)) for _ in range(3)]
    await generate_images(queue, filenames)
    await queue.join()

    # Clean up consumers
    for consumer in consumers:
        consumer.cancel()

    await asyncio.gather(*consumers, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
