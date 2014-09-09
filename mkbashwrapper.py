#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate shell scripts that run Python scripts.

Example:
  You run this with
"""

import sys
import os
import glob
from argparse import ArgumentParser
from jinja2 import Environment

__version__ = '0.0.1'

# Constant values.
NEWLINE_SEQUENCE = '\n'
PATTERN = '*.py'
BASH_TEMPLATE = '''\
#!/bin/bash

/usr/bin/env python '{{ PY_SCRIPT_NAME }}' $@
'''

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(
        description="Generate shell scripts for Python scripts.")
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        '-d', '--directory',
        default='.',
        help='target directory (default to current directory)')

    return parser

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    directory = args.directory
    os.chdir(directory)

    workdir = os.path.realpath(directory)

    env = Environment(newline_sequence=NEWLINE_SEQUENCE)
    template = env.from_string(BASH_TEMPLATE)

    for name in glob.iglob(PATTERN):
        process(template, workdir, name)

def process(template, outdir, pyname):
    """The core function.

    Args:
        template: A template text for Bash script.
        outdir: A directory shell scripts will be generated in.
        pyname: A Python script.

    Returns:
        None.
    """

    name, ext = os.path.splitext(pyname)
    if ext == '.py':
        shname = os.path.join(outdir, name + '.sh')
        with open(shname, mode='w', newline=NEWLINE_SEQUENCE) as fout:
            fout.write(template.render(
                PY_SCRIPT_NAME=os.path.realpath(pyname)))
            fout.write(NEWLINE_SEQUENCE)
            print('Processed {0}'.format(shname), file=sys.stderr)

if __name__ == '__main__':
    main(configure().parse_args())
