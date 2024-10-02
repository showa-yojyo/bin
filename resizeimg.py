#!/usr/bin/env python

"""
Make landscape image files portrait.
"""

import asyncio
from tkinter import Tk
import math
import sys
from typing import Callable, Iterable, Optional
from PIL import Image


# python - How could I find the resolution of a display running Python3 on Linux? - Stack Overflow
# <https://stackoverflow.com/questions/64189320/how-could-i-find-the-resolution-of-a-display-running-python3-on-linux>
def _determine_portrait_size() -> tuple[int, int]:
    """Determine the dimension of portrait"""
    root = Tk()
    root.withdraw()
    screen_height, screen_width = (
        root.winfo_screenheight(), root.winfo_screenwidth())
    if screen_width <= screen_height:
        return (screen_width, screen_height)
    else:
        return (screen_height, screen_width)

SIZE_PORTRAIT = _determine_portrait_size()

def round_aspect(
    number: float,
    key: Callable[[int], float]) -> int:
    """(code taken from PIL)"""
    return max(min(math.floor(number), math.ceil(number), key=key), 1)


def fit_to_screen(width: int, height: int) -> tuple[int, int]:
    """(code taken from PIL)"""

    x: int
    y: int
    if width < height:
        x, y = SIZE_PORTRAIT
    else:
        y, x = SIZE_PORTRAIT

    # preserve aspect ratio
    aspect: float = width / height
    if x / y >= aspect:
        x = round_aspect(y * aspect, key=lambda n: abs(aspect - n / y))
    else:
        y = round_aspect(x / aspect, key=lambda n: abs(aspect - x / n))
    return (x, y)

async def generate_images(
    queue: asyncio.Queue,
    filenames: Iterable[str]) -> None:
    """Producer coroutine"""

    for name in filenames:
        #print(f'Producing {name}')
        await queue.put((name, Image.open(name)))


def process_image(image: Image.Image):
    width_old, height_old = image.width, image.height
    size_new = fit_to_screen(width_old, height_old)

    use_resize = False
    if width_old > height_old:
        # case of landscape
        use_resize = width_old < SIZE_PORTRAIT[1]
    else:
        # case of portrait
        use_resize = height_old < SIZE_PORTRAIT[1]

    resize_args = (size_new, Image.Resampling.LANCZOS)
    if use_resize:
        image = image.resize(*resize_args)
    else:
        image.thumbnail(*resize_args)

    return image

async def process_images(queue: asyncio.Queue) -> None:
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

async def main(filenames: Iterable[str]) -> None:
    """main entry point"""

    # Producer/consumer pattern
    queue: asyncio.Queue = asyncio.Queue()

    # XXX: the number of consumers shuold be variable
    consumers = [asyncio.create_task(process_images(queue)) for _ in range(3)]
    await generate_images(queue, filenames)
    await queue.join()

    # Clean up consumers
    for consumer in consumers:
        consumer.cancel()

    await asyncio.gather(*consumers, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
