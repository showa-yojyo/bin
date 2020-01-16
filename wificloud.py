#!/usr/bin/env python

"""Automate Internet connection for wifi-cloud.jp
"""

from argparse import ArgumentParser
import sys

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

__version__ = '1'

PORTAL_URL = 'http://www.wifi-cloud.jp/'
PAGE1_CSS_SELECTOR = 'p#btn_connect > a'
PAGE2_NAME = 'form1'
SPOT_MAP = {
    'koto': '江東区',
    'shinagawa': '品川区',}

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
        help='"koto" or "shinagawa"')

    return parser.parse_args(args or ['--help'])

def run(args):
    """Make the WebDriver connect to FLET'S Wi-Fi"""

    driver = webdriver.Edge()
    driver.implicitly_wait(20)
    try:
        driver.get(PORTAL_URL)

        # Connect to Internet
        driver.get(driver.find_element_by_css_selector(
            PAGE1_CSS_SELECTOR).get_attribute('href'))

        # Agree
        driver.find_element_by_name(PAGE2_NAME).submit()

        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.title_contains(
            SPOT_MAP.get(args.where, '区')))
    finally:
        driver.close()

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
