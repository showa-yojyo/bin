#!/usr/bin/env python

from argparse import ArgumentParser
from urllib import request
from pprint import pprint
import sys
from bs4 import BeautifulSoup

__version__ = '1.0.0'

def parse_args(args):
    """Parse the command line parameters."

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='href extractor')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        '--format',
        default='pprint',
        help='output format'
    )

    parser.add_argument(
        'url',
        help='URL from which to extract href values')

    return parser.parse_args(args or [])

def run(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
        function.

    Returns:
        None.
    """

    url = args.url
    # download the file
    with request.urlopen(url) as fin:
        data = fin.read()

    # create an instance of bs
    bs = BeautifulSoup(data, 'html.parser')
    links = bs.find_all('a')
    processed = [(i.get('href'), i.text) for i in links]

    if args.format == 'pprint':
        pprint(processed)
    elif args.format == 'csv':
        print('URL\ttext')
        for i in processed:
            print('\t'.join(i))

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == "__main__":
    main()
