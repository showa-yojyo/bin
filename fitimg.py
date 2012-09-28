# -*- coding: utf-8 -*-
u"""
Copyright (c) 2012 プレハブ小屋 <yojyo@hotmail.com>
All Rights Reserved.  NO WARRANTY.

Resizes larger JPEG files in the current directory to 1024x768 size
(aspect ratio will be preserved).
"""

import sys
import glob
# PIL
import Image

PATTERN = '*.jpg'
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

def main():
    for name in glob.iglob(PATTERN):
        process(name)

def process(jpg):
    try:
        img = Image.open(jpg)
        sz = img.size
        if sz[0] <= SCREEN_WIDTH and sz[1] <= SCREEN_HEIGHT:
            sys.stderr.write('Skipped: {0} ({1[0]}x{1[1]})\n'.format(jpg, sz))
            return

        newsz = (min(sz[0], SCREEN_WIDTH), min(sz[1], SCREEN_HEIGHT))
        img.thumbnail(newsz, Image.ANTIALIAS)
        img.save(jpg)
        sys.stderr.write('Resized: {0} ({1[0]}x{1[1]})\n'.format(jpg, img.size))
    except Exception as e:
        sys.stderr.write('{0}\n'.format(e))

if __name__ == '__main__':
    main()
