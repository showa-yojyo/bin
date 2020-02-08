#!/usr/bin/env python

import sys
from hashlib import md5
from os import rename
from os.path import dirname, join, splitext

def newname(data, oldname):
    h = md5()
    h.update(data)
    newbasename = h.hexdigest()

    oldbasename, extension = splitext(oldname)
    return join(dirname(oldname), newbasename + extension)
    #return dir + '/' + basename + extension
    #return oldname.replace(oldbasename, newbasename)

def main(args=sys.argv[1:]):
    #sys.exit(run(parse_args(args)))

    for i in args:
        with open(i, 'rb') as input:
            data = input.read()
            name = newname(data, i)

        rename(i, name)
        #print(i, name)

if __name__ == '__main__':
    main()
