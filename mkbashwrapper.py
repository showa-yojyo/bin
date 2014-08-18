# -*- coding: utf-8 -*-
"""Copyright (c) 2012 プレハブ小屋 <yojyo@hotmail.com>
All Rights Reserved.  NO WARRANTY.
"""

import sys
import os
import glob
from argparse import ArgumentParser
from jinja2 import Environment

__version__ = '0.0.0'

NEWLINE_SEQUENCE='\n'
PATTERN = '*.py'
BASH_TEMPLATE = '''\
#!/bin/bash

/usr/bin/env python '{{ PY_SCRIPT_NAME }}' $@
'''

def main(args):
    # get target directory
    directory = args.directory
    os.chdir(directory)

    dir = os.path.realpath(directory)

    env = Environment(newline_sequence=NEWLINE_SEQUENCE)
    template = env.from_string(BASH_TEMPLATE)

    for name in glob.iglob(PATTERN):
        process(template, dir, name)

def process(template, dir, pyname):
    try:
        name, ext = os.path.splitext(pyname)
        if ext == '.py':
            shname = os.path.join(dir, name + '.sh')
            kwargs = dict(PY_SCRIPT_NAME=os.path.realpath(pyname))
            with open(shname, 'wb') as fout:
                fout.write(
                    template.render(**kwargs))
                fout.write(NEWLINE_SEQUENCE)
                sys.stderr.write('Processed {0}\n'.format(shname))

    except Exception as e:
        sys.stderr.write('{0}\n'.format(e))

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__, version=__version__)
    parser.add_argument(
        '-d','--directory',
        default='.',
        help='target directory (default to current directory)')
    args = parser.parse_args()
    main(args)
