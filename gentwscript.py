#!/usr/bin/env python
"""gentwscript.py A temporary script to generate skeleton.
"""
from argparse import (ArgumentParser, FileType)
from json import load
import sys
from jinja2 import (Environment, FileSystemLoader)

__version__ = '0.0.1'

def parse_args(args):
    """Parse the command line parameters."""

    root_parser = ArgumentParser()
    root_parser.add_argument(
        '--version',
        action='version',
        version=__version__)

    file_parser = ArgumentParser(add_help=False)
    file_parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        type=FileType('r', encoding='utf-8'),
        help='JSON')

    subparsers = root_parser.add_subparsers(help='commands')
    parser = subparsers.add_parser(
        'twmods',
        parents=[file_parser],
        help='generate both skeleton scripts and modules for twmods')
    parser.set_defaults(func=twmods)

    parser = subparsers.add_parser(
        'pttdemo',
        parents=[file_parser],
        help='generate scripts for PTT demonstration')
    parser.set_defaults(func=pttdemo)

    return root_parser.parse_args(args=args or ('--help',))

def twmods(env, json_data):
    """Generate skeleton for twmods/commands modules and their driver
    scripts.
    """

    tmpl_script = env.get_template('twscript.py_t')
    tmpl_command_module = env.get_template('command.py_t')

    for kwargs in json_data:
        # Generate a script file.
        with open(f'''tw{kwargs['basename']}.py''',
                  mode='w', newline='') as fout:
            fout.write(tmpl_script.render(**kwargs))
            fout.write('\n')

        # Generate a module file.
        with open(f'''twmods/commands/{kwargs['command_module']}.py''',
                  mode='w', newline='') as fout:
            fout.write(tmpl_command_module.render(**kwargs))
            fout.write('\n')

def pttdemo(env, json_data):
    """Generate skeleton for scripts under notebooks/source/_sample/ptt
    and reST files under notebooks/source/python-twitter.
    """

    tmpl_script = env.get_template('pttdemo.py_t')
    tmpl_rst = env.get_template('rest-api.rst_t')
    for kwargs in json_data:
        endpoints = kwargs['endpoints']

        # file name e.g. GET direct_messages/show -> rest-direct-messages.rst
        one_name = endpoints[0].split(' ')[-1].replace('_', '-')
        rst_name = f'''rest-{one_name.partition('/')[0]}.rst'''

        with open(rst_name, mode='w', encoding='utf-8', newline='') as fout:
            fout.write(tmpl_rst.render(**kwargs))
            fout.write('\n')

        for i in endpoints:
            # file name e.g. POST lists/memberships/create
            # -> lists-memberships-create.py
            file_name = i.split(' ')[1].replace('/', '-').replace(':', '')
            with open(f'{file_name}.py', mode='w', newline='') as fout:
                fout.write(tmpl_script.render(endpoint=i))
                fout.write('\n')

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args=args)))

def run(args):
    """The main function."""

    args.func(
        Environment(
            loader=FileSystemLoader('twtmpl', encoding='utf-8'),
            autoescape=False),
        load(args.file))

if __name__ == '__main__':
    main()
