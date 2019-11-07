#!/usr/bin/env python

"""Automate Free Wi-Fi confirmation
"""
from selenium import webdriver

WIFI_URL = 'http://www.e-flets.jp/disaster'
#WIFI_URL = "file://C:/cygwin64/tmp/portal2.html"

def main():
    """Do everything"""

    driver = webdriver.Edge()
    driver.get(WIFI_URL)

    # The checkbox "I agree with the terms of use"
    agreed = driver.find_element_by_id('radio-use')
    assert not agreed.is_selected()
    agreed.click()

    # The button "To confirmation screen"
    button = driver.find_element_by_name('loginBtn')
    button.click() # submit

    driver.close()

if __name__ == '__main__':
    main()
