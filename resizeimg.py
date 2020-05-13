#!/usr/bin/env python

"""
Make landscape image files portrait.
"""

import asyncio
import math
import sys
import ctypes
from PIL import Image


def _determine_portrait_size():
    """Determine the dimension of portrait"""

    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    if screen_width <= screen_height:
        return (screen_width, screen_height)

    return (screen_height, screen_width)

# XXX: Windows only...
SIZE_PORTRAIT = _determine_portrait_size()

def round_aspect(number, key):
    """(code taken from PIL)"""
    return max(min(math.floor(number), math.ceil(number), key=key), 1)


def fit_to_screen(width, height):
    """(code taken from PIL)"""

    if width < height:
        x, y = SIZE_PORTRAIT
    else:
        y, x = SIZE_PORTRAIT

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
    size_new = fit_to_screen(width_old, height_old)

    use_resize = False
    if width_old > height_old:
        # case of landscape
        use_resize = width_old < SIZE_PORTRAIT[1]
    else:
        # case of portrait
        use_resize = height_old < SIZE_PORTRAIT[1]

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
