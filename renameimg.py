#!/usr/bin/env python

import sys
from hashlib import md5
from os import (remove, rename)
from os.path import (dirname, join, splitext)

def newname(data, oldname):
    h = md5()
    h.update(data)
    newbasename = h.hexdigest()

    oldbasename, extension = splitext(oldname)
    return join(dirname(oldname), newbasename + extension)

def main(args=sys.argv[1:]):
    for oldname in args:
        with open(oldname, 'rb') as input:
            data = input.read()
        try:
            rename(oldname, newname(data, oldname))
        except FileExistsError:
            remove(oldname)

if __name__ == '__main__':
    main()
