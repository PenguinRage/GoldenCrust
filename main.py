from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException

import time
from enum import Enum
# Check version in Brave: brave://version/
# Chromedriver location: https://sites.google.com/a/chromium.org/chromedriver/
# we need to freeze this.......
from selenium.webdriver.support import expected_conditions, wait

# Browser config
driver_path = "./chromedriver"
brave_path = "/usr/lib/brave/brave"
option = Options()
option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless")


class meal(Enum):
    FAMILY = '//*[@id="meal-combos"]/ul/li[3]/a/div/span'
    ME = '//*[@id="meal-combos"]/ul/li[2]/a/div/span'


def fill_address_details(driver):
    driver.get('https://orders.eatapp.online/menu/golden-crust-baulkham-hills#ordering-for-prompt')
    try:
        driver.find_element_by_xpath('//*[@id="start-order-type"]/div[1]/div[2]/button[3]').click()
        driver.find_element_by_xpath('//*[@id="start-delivery-address"]').send_keys("123 Fake Drive")
        driver.find_element_by_xpath('//*[@id="start-delivery-address-line2"]').send_keys("Seven Hills")
        driver.find_element_by_xpath('//*[@id="start-delivery-zip"]').send_keys("1234")
        driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[2]/button[1]').click()
        driver.find_element_by_xpath('//*[@id="start-order"]').click()
    except ElementClickInterceptedException:
        print(driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[3]').text)
        exit(1)
    time.sleep(5)


def get_order(driver):
    driver.find_element_by_link_text('Meal Combos').click()
    time.sleep(1)
    driver.find_element_by_xpath(meal.FAMILY.value).click()


driver = webdriver.Chrome(options=option, executable_path=driver_path)
fill_address_details(driver)
get_order(driver)



