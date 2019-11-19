#!/usr/bin/env python

"""Automate confirmation for Ota_City_Free_Wi-Fi_1
"""
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

FLETS_PORTAL_URL = 'http://www.e-flets.jp/'

PAGE_1_CSS_SELECTOR = 'a[checkID="2300"]'
PAGE_2_CSS_SELECTOR = 'a[checkID="2310"]'
PAGE_3_RADIO_ID = 'radio-use'
PAGE_3_BUTTON_NAME = 'loginBtn'

def main():
    """Make the WebDriver connect to FLET'S Wi-Fi"""

    driver = webdriver.Edge()
    driver.implicitly_wait(20)
    try:
        driver.get(FLETS_PORTAL_URL)

        # Click "Wi-Fi" and then "Free Wi-Fi Internet"
        for i in (PAGE_1_CSS_SELECTOR, PAGE_2_CSS_SELECTOR):
            elem = driver.find_element_by_css_selector(i)
            url = elem.get_attribute('href')
            driver.get(url)

        # The checkbox "I agree with the terms of use"
        agreed = driver.find_element_by_id(PAGE_3_RADIO_ID)
        agreed.click()
        assert agreed.is_selected()

        # The button "To confirmation screen"
        driver.find_element_by_name(PAGE_3_BUTTON_NAME).click()

        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.title_contains(
            '大田区立図書館'))
    except Exception:
        breakpoint()
        raise
    finally:
        driver.close()

if __name__ == '__main__':
    main()
