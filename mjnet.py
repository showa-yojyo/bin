#!/usr/bin/env python

"""mjnet.py: (under construction)
"""

import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

MJ_NET_URL = 'https://www.sega-mj.net/mjac_p'
MJ_NET_URL_SIGN_IN = MJ_NET_URL + '/mjlogin/login.jsp'
MJ_NET_URL_SIGN_OUT = MJ_NET_URL + '/FwdPage?page=logout'
MJ_NET_URL_TOP_PAGE = MJ_NET_URL + '/FwdPage?page=top'
MJ_NET_URL_PLAYER_DATA_PAGE = MJ_NET_URL + '/FwdPage?page=playdata&i=0'

def main():
    """The function invoked when the program is executed"""

    if len(sys.argv) < 3:
        print("Usage: mjnet.py USER_NAME PASSWORD", file=sys.stderr)
        sys.exit(2)

    driver = webdriver.Edge()
    driver.implicitly_wait(20)
    sign_in(driver, sys.argv[1], sys.argv[2])
    try:
        go_to_top(driver)
        go_to_play_data(driver)
        go_to_tompu_pro(driver)
        go_to_daily_record(driver)
        print('*'*80)
        print_current_contents(driver)
        sign_out(driver)
    except Exception:
        breakpoint()
        raise
    finally:
        driver.close()

def pause(func):
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

@pause
def go_to_top(driver):
    """Move to the top page"""
    driver.get(MJ_NET_URL_TOP_PAGE)

@pause
def go_to_play_data(driver):
    """Move to プレイデータ"""
    driver.get(MJ_NET_URL_PLAYER_DATA_PAGE)

@pause
def go_to_tompu_pro(driver):
    """Move to プロ卓東風戦"""

    wait = WebDriverWait(driver, 60)
    wait.until(
        expected_conditions.visibility_of_all_elements_located(
            (By.LINK_TEXT, '東風戦')))

    links = driver.find_elements_by_link_text('東風戦')
    assert len(links) >= 2
    driver.get(links[1].get_attribute('href'))


@pause
def go_to_daily_record(driver):
    """Move to デイリー戦績"""

    elem = driver.find_element_by_link_text('デイリー戦績')
    driver.get(elem.get_attribute('href'))

def print_current_contents(driver):
    """Output an innerText"""

    # trim the first lines and the last lines
    print('\n'.join(driver.find_element_by_css_selector(
        'div.common-wrap').text.splitlines()[3:-3]))

if __name__ == "__main__":
    main()
