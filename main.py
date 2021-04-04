from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException

import time
from enum import Enum
# Check version in Brave: brave://version/
# Chromedriver location: https://sites.google.com/a/chromium.org/chromedriver/
# we need to freeze this.......

# Browser config
from selenium.webdriver.support.wait import WebDriverWait

driver_path = "./chromedriver"
brave_path = "/usr/lib/brave/brave"
option = Options()
option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless")


# Todo: Move this logic else where. Responsibility could be given to a builder
# Todo: Secure credentials/home details elsewhere
# TODO: Fix website is drastically changed on this day, logic for ordering a deal is different
class pizza(Enum):
    MEATLOVERS = '//*[@id="menu"]/span/div[11]/ul[2]/li[9]/a/div[2]/h3'
    PERIPERI = '//*[@id="menu"]/span/div[11]/ul[2]/li[34]/a/div[2]/h3'
    PEPPERONI = '//*[@id="menu"]/span/div[11]/ul[2]/li[15]/a/div[2]/h3'
    SPICYCHICKEN = '//*[@id="menu"]/span/div[11]/ul[2]/li[16]/a/div[2]/h3'


class meal(Enum):
    ME = '//*[@id="meal-combos"]/ul/li[2]/a/div/span'
    FAMILY = '//*[@id="meal-combos"]/ul/li[3]/a/div/span'


class sides(Enum):
    GARLICBREAD = '//*[@id="menu"]/span/div[11]/ul[2]/li[1]/a/div[2]'


class drinks(Enum):
    PEPSIMAX = '//*[@id="menu"]/span/div[11]/ul[2]/li[4]/a'


def fill_address_details():
    driver.get('https://orders.eatapp.online/menu/golden-crust-baulkham-hills#ordering-for-prompt')
    try:
        driver.find_element_by_xpath('//*[@id="start-order-type"]/div[1]/div[2]/button[3]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="start-delivery-address"]').send_keys("19 Allandale Drive")
        driver.find_element_by_xpath('//*[@id="start-delivery-address-line2"]').send_keys("Baulkham Hills")
        driver.find_element_by_xpath('//*[@id="start-delivery-zip"]').send_keys("2153")
        driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[2]/button[1]').click()
        driver.find_element_by_xpath('//*[@id="start-order"]').click()
    except ElementClickInterceptedException:
        print("Exception:" + driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[3]').text)
        exit(1)
    time.sleep(5)


def get_order():
    try:
        driver.find_element_by_link_text('Meal Combos').click()
    except NoSuchElementException:
        print("KNOWN BUG: Tuesdays Special offerings break here")
        driver.close()
        exit(2)
    time.sleep(1)
    driver.find_element_by_xpath(meal.ME.value).click()
    add_to_order(pizza.MEATLOVERS)
    add_to_order(sides.GARLICBREAD)
    add_to_order(drinks.PEPSIMAX)


def add_to_order(item):
    time.sleep(5)
    element = WebDriverWait(driver, 10).until(
        lambda finder: finder.find_element_by_xpath(item.value))
    element.click()
    time.sleep(5)
    try:
        element = WebDriverWait(driver, 10).until(
            lambda finder: finder.find_element_by_xpath('//*[@id="menu-app"]/div[13]/div/div/form/div[2]/button[3]'))
        element.click()
    except ElementNotInteractableException:
        element = WebDriverWait(driver, 10).until(
            lambda finder: finder.find_element_by_xpath('//*[@id="menu-app"]/div[13]/div/div/form/div[2]/button[1]/span'))
        element.click()


driver = webdriver.Chrome(options=option, executable_path=driver_path)
fill_address_details()
get_order()

