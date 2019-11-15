#!/usr/bin/env python

"""mjnet.py: (under construction)
"""

import sys
from selenium import webdriver

MJ_NET_URL = 'https://www.sega-mj.net/mjac_p'
MJ_NET_URL_SIGN_IN = MJ_NET_URL + '/mjlogin/login.jsp'
MJ_NET_URL_SIGN_OUT = MJ_NET_URL + '/FwdPage?page=logout'

def main():
    """The function invoked when the program is executed"""

    if len(sys.argv) < 2:
        print("Usage: mjnet.py USER_NAME PASSWORD", file=sys.stderr)
        sys.exit(2)

    driver = webdriver.Edge()
    sign_in(driver, sys.argv[0], sys.argv[1])
    try:
        #go_to_top(driver) # FIXME
        go_to_play_data(driver)
        go_to_tompu_pro(driver)
        go_to_daily_record(driver)
        print(get_daily_record(driver))
    finally:
        sign_out(driver)
        driver.close()

def sign_in(driver, user_name, password):
    """Sign in MJ.NET"""

    driver.get(MJ_NET_URL_SIGN_IN)
    driver.find_element_by_name('uid').send_keys(user_name)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_tag_name('form').submit()

def sign_out(driver):
    """Sign out of MJ.NET"""
    driver.get(MJ_NET_URL_SIGN_OUT)

def go_to_top(driver):
    """FIXME"""
    driver.find_element_by_css_selector('a[accesskey="0"]').click()

def go_to_play_data(driver):
    """Move to プレイデータ"""
    driver.find_element_by_class_name('player-status-basic').click()

def go_to_tompu_pro(driver):
    """Move to プロ卓東風戦"""
    links = driver.find_elements_by_link_text('東風戦')
    assert len(links) > 2
    links[1].click()

def go_to_daily_record(driver):
    """Move to デイリー戦績"""
    driver.find_elements_by_link_text('デイリー戦績').click()

def get_daily_record(driver):
    """Return the daily record"""
    return driver.find_element_by_css_selector('div.common-wrap')

if __name__ == "__main__":
    main()
