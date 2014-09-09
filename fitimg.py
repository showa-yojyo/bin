#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resize large JPEG files in the current directory down to the screen
resolution size with its aspect ratio preserved.

Examples:
  You just call this script without arguments::

    $ python fitimg.py
"""

import sys
import glob
from argparse import ArgumentParser
# PIL
from PIL import Image

__version__ = '1.0.1'

# Constant values.
PATTERN = '*.jpg'
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """
    parser = ArgumentParser(
        description='Resize large JPEG files to the screen size')
    parser.add_argument('--version', action='version', version=__version__)
    return parser

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    for name in glob.iglob(PATTERN):
        process(name)

def process(jpg):
    """The main function.

    Args:
        jpg: A path to JPEG file.

    Returns:
        None.
    """

    img = Image.open(jpg)
    extent = img.size
    if extent[0] <= SCREEN_WIDTH and extent[1] <= SCREEN_HEIGHT:
        print('Skipped: {0} ({size[0]}x{size[1]})'.format(jpg, size=extent),
              file=sys.stderr)
        return

    new_extent = (min(extent[0], SCREEN_WIDTH), min(extent[1], SCREEN_HEIGHT))
    img.thumbnail(new_extent, Image.ANTIALIAS)
    img.save(jpg)
    print('Resized: {0} ({size[0]}x{size[1]})'.format(jpg, size=img.size),
          file=sys.stderr)

if __name__ == '__main__':
    main(configure().parse_args())
