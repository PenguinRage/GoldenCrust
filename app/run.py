from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

import time
from enum import Enum
# Check version in Brave: brave://version/
# Chromedriver location: https://sites.google.com/a/chromium.org/chromedriver/
# we need to freeze this.......
import argparse
from dao.bitwardenDAO import BitwardenDAO
from selenium.webdriver.support.ui import WebDriverWait


driver_path = "/usr/lib/brave/chromedriver"
brave_path = "/usr/lib/brave/brave"
option = Options()
option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless")


# Todo: Move this logic else where. Responsibility could be given to a builder
# TODO: Fix website is drastically changed on this day, logic for ordering a deal is different
class meal(Enum):
    ME = '//*[@id="meal-combos"]/ul/li[2]/a/div/span' #//*[@id="meal-combos-tuesday"]/ul/li[2]/a/div/h3
    FAMILY = '//*[@id="meal-combos"]/ul/li[3]/a/div/span' # '//*[@id="meal-combos-tuesday"]/ul/li[3]/a/div/span'


class pizza(Enum):
    MEATLOVERS = '//*[@id="menu"]/span/div[11]/ul[2]/li[9]/a/div[2]/h3'
    PERIPERI = '//*[@id="menu"]/span/div[11]/ul[2]/li[34]/a/div[2]/h3'
    PEPPERONI = '//*[@id="menu"]/span/div[11]/ul[2]/li[15]/a/div[2]/h3'
    SPICYCHICKEN = '//*[@id="menu"]/span/div[11]/ul[2]/li[16]/a/div[2]/h3'


class sides(Enum):
    GARLICBREAD = '//*[@id="menu"]/span/div[11]/ul[2]/li[1]/a/div[2]'


class drinks(Enum):
    PEPSIMAX = '//*[@id="menu"]/span/div[11]/ul[2]/li[4]/a'


def fill_address_details():
    driver.get('https://orders.eatapp.online/menu/golden-crust-baulkham-hills#ordering-for-prompt')
    try:
        credentials = BitwardenDAO.get_item('b4651e5a-157a-45b0-84e6-ad1e00d1a8f5')
        driver.find_element_by_xpath('//*[@id="menu-app"]/div[7]/div/div/div/div/button').click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('/html/body/div[1]/div[7]/div/div/div/div/form/div[2]/input').send_keys(credentials['login']['username'])
        driver.find_element_by_xpath('/html/body/div[1]/div[7]/div/div/div/div/form/div[3]/input').send_keys(credentials['login']['password'])
        driver.find_element_by_xpath('/html/body/div[1]/div[7]/div/div/div/div/form/div[4]/button').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="start-order-type"]/div[1]/div[2]/button[3]').click()
        driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[2]/button[1]').click()
        driver.find_element_by_xpath('//*[@id="start-order"]').click()
    except ElementClickInterceptedException:
        print("Exception: " + driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[3]').text)

    time.sleep(5)


def get_order():
    driver.find_element_by_partial_link_text('Meal Combos').click()
    time.sleep(1)
    driver.find_element_by_xpath(meal.FAMILY.value).click()
    add_to_order(pizza.MEATLOVERS)
    add_to_order(pizza.PEPPERONI)
    add_to_order(sides.GARLICBREAD)
    add_to_order(drinks.PEPSIMAX)
    time.sleep(5)
    select_button_by_link_text('Check Out')
    complete_order()


def add_to_order(item):
    time.sleep(5)
    element = WebDriverWait(driver, 10).until(
        lambda finder: finder.find_element_by_xpath(item.value))
    element.click()
    time.sleep(5)
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div[12]/div/div/form/div[2]/button[3]/span').click()
    except ElementNotInteractableException:
        driver.find_element_by_xpath('/html/body/div[1]/div[12]/div/div/form/div[2]/button[1]/span').click()


def complete_order():
    driver.find_element_by_xpath('//*[@id="custom_field_suburb"]').send_keys('Baulkham Hills')
    select_button_by_link_text("No tip")
    driver.find_element_by_xpath('//*[@id="checkout-form"]/div[3]/button').click()


def select_button_by_link_text(text):
    element = WebDriverWait(driver, 10).until(
        lambda finder: finder.find_element_by_link_text(text))
    element.click()


driver = webdriver.Chrome(options=option, executable_path=driver_path)
fill_address_details()
get_order()

