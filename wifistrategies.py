"""wifistrategies.py"""

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

_REGISTRY_MAP = dict()

def get_controller(where):
    """Return the most suitable function

    Args:
        where: 'koto', 'shinagawa', etc.
    """

    try:
        return _REGISTRY_MAP[where]
    except KeyError:
        class WiFiNotSupported(NotImplementedError):
            """Not yet supported"""

        raise WiFiNotSupported("Unknown area")

def register(where):
    """Strategy pattern"""

    def decorate(func):
        _REGISTRY_MAP[where] = func
        return func
    return decorate

PORTAL_URL = 'http://www.wifi-cloud.jp/'
PAGE1_CSS_SELECTOR = 'p#btn_connect > a'
PAGE2_NAME = 'form1'

@register('koto')
def connect_koto(driver):
    """Connect Free Wi-Fi for 江東区"""

    connect_free_wifi(driver, '江東区')

@register('shinagawa')
def connect_shinagawa(driver):
    """Connect Free Wi-Fi for 品川区"""

    connect_free_wifi(driver, '品川区')

def connect_free_wifi(driver, title):
    """Common process to Wi-Fi cloud"""

    driver.get(PORTAL_URL)

    # Connect to Internet
    driver.get(driver.find_element_by_css_selector(
        PAGE1_CSS_SELECTOR).get_attribute('href'))

    # Agree
    driver.find_element_by_name(PAGE2_NAME).submit()

    wait = WebDriverWait(driver, 60)
    wait.until(expected_conditions.title_contains(title))

FLETS_PORTAL_URL = 'http://www.e-flets.jp/'

PAGE_1_CSS_SELECTOR = 'a[checkID="2300"]'
PAGE_2_CSS_SELECTOR = 'a[checkID="2310"]'
PAGE_3_RADIO_ID = 'radio-use'
PAGE_3_BUTTON_NAME = 'loginBtn'

@register('ota')
def connect_ota(driver):
    """Connect Free Wi-Fi for 大田区"""

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
