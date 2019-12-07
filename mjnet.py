#!/usr/bin/env python

"""mjnet.py: (under construction)
"""

import sys
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

__version__ = '1.?'

MJ_NET_URL = 'https://www.sega-mj.net/mjac_p'
MJ_NET_URL_SIGN_IN = MJ_NET_URL + '/mjlogin/login.jsp'
MJ_NET_URL_SIGN_OUT = MJ_NET_URL + '/FwdPage?page=logout'
MJ_NET_URL_TOP_PAGE = MJ_NET_URL + '/FwdPage?page=top'
MJ_NET_URL_PLAYER_DATA_PAGE = MJ_NET_URL + '/FwdPage?page=playdata&i=0'

def parse_args(args):
    """Parse the command line parameters."

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(
        description='automation script for access to MJ.NET')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        'user_name',
        help='account name for MJ.NET')
    parser.add_argument(
        'password',
        help='passowrd for user_name')
    parser.add_argument(
        '-p', '--pause',
        action='store_true',
        default=False,
        help='pause before closing browser')
    parser.add_argument(
        '--only-login',
        action='store_true',
        default=False,
        help='only sign in MJ.NET')
    return parser.parse_args(args or ['--help'])


def run(args):
    """The function invoked when the program is executed"""

    pause = args.pause
    driver = webdriver.Edge()
    driver.implicitly_wait(20)
    sign_in(driver, args.user_name, args.password)
    if args.only_login:
        return

    try:
        go_to_top(driver)
        go_to_play_data(driver)
        go_to_tompu_pro(driver)
        go_to_daily_record(driver)
        print('*'*80)
        print_current_contents(driver)
        if pause:
            input('Pause. Press any key to continue:')
        sign_out(driver)
    except Exception:
        breakpoint()
        raise
    finally:
        driver.close()

def hook(func):
    """debugging"""
    def wrapper(driver):
        #print(func.__name__)

        actions = ActionChains(driver)
        actions.send_keys(Keys.HOME)
        actions.send_keys(Keys.END)
        actions.perform()

        return func(driver)
    return wrapper

def sign_in(driver, user_name, password):
    """Sign in MJ.NET"""

    driver.get(MJ_NET_URL_SIGN_IN)
    driver.find_element_by_name('uid').send_keys(user_name)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_tag_name('form').submit()

def sign_out(driver):
    """Sign out of MJ.NET"""
    driver.get(MJ_NET_URL_SIGN_OUT)

@hook
def go_to_top(driver):
    """Move to the top page"""
    driver.get(MJ_NET_URL_TOP_PAGE)

@hook
def go_to_play_data(driver):
    """Move to プレイデータ"""
    driver.get(MJ_NET_URL_PLAYER_DATA_PAGE)

@hook
def go_to_tompu_pro(driver):
    """Move to プロ卓東風戦"""

    wait = WebDriverWait(driver, 60)
    wait.until(
        expected_conditions.visibility_of_all_elements_located(
            (By.LINK_TEXT, '東風戦')))

    links = driver.find_elements_by_link_text('東風戦')
    assert len(links) >= 2
    driver.get(links[1].get_attribute('href'))


@hook
def go_to_daily_record(driver):
    """Move to デイリー戦績"""

    elem = driver.find_element_by_link_text('デイリー戦績')
    driver.get(elem.get_attribute('href'))

def print_current_contents(driver):
    """Output an innerText"""

    # trim the first lines and the last lines
    print('\n'.join(driver.find_element_by_css_selector(
        'div.common-wrap').text.splitlines()[3:-3]))

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == "__main__":
    main()
