#!/usr/bin/env python

"""Automate Free Wi-Fi confirmation
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

FLETS_PORTAL_URL = 'http://www.e-flets.jp/'

PAGE_1_CSS_SELECTOR = 'a[checkID="2300"] > h2 > img'
PAGE_2_RADIO_ID = 'radio-use'
PAGE_2_BUTTON_NAME = 'loginBtn'

def main():
    """Make the WebDriver connect to FLET'S Wi-Fi"""

    driver = webdriver.Edge()
    try:
        driver.get(FLETS_PORTAL_URL)

        # Click the banner "Wi-Fi"
        driver.find_element_by_css_selector(
            PAGE_1_CSS_SELECTOR).click()

        WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located(
            (By.NAME, PAGE_2_BUTTON_NAME)))

        # The checkbox "I agree with the terms of use"
        agreed = driver.find_element_by_id(PAGE_2_RADIO_ID)
        agreed.click()
        assert agreed.is_selected()

        # The button "To confirmation screen"
        driver.find_element_by_name(PAGE_2_BUTTON_NAME).click()

        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.title_contains(
            '大田区公式観光サイト'))
    finally:
        driver.close()

if __name__ == '__main__':
    main()
