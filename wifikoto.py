#!/usr/bin/env python

"""Automate confirmation for Koto_City_Free_Wi-Fi
"""
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

PORTAL_URL = 'http://www.wifi-cloud.jp/'
PAGE1_CSS_SELECTOR = 'p#btn_connect > a'
PAGE2_NAME = 'form1'

def main():
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
        wait.until(expected_conditions.title_contains('江東区'))
    except Exception:
        breakpoint()
        raise
    finally:
        driver.close()

if __name__ == '__main__':
    main()
