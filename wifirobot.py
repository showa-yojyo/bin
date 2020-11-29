#!/usr/bin/env python

"""Automate Internet connection for Free Wi-Fi
"""

from argparse import ArgumentParser
import sys

from selenium import webdriver
from wifistrategies import get_controller

__version__ = '2'

def parse_args(args):
    """Parse the command line parameters."

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Free Wi-Fi connection')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        'where',
        choices=("koto", "shinagawa", "ota"),
        help='which area is here')

    return parser.parse_args(args or ['--help'])

def run(args):
    """Make the WebDriver connect to Free Wi-Fi"""

    driver = webdriver.Edge()
    try:
        driver.implicitly_wait(20)
        controller = get_controller(args.where)
        controller(driver)
    finally:
        driver.close()

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
