from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

import time
from enum import Enum
# Check version in Brave: brave://version/
# Chromedriver location: https://sites.google.com/a/chromium.org/chromedriver/
# we need to freeze this.......
import pickledb
# Browser config
from selenium.webdriver.support.wait import WebDriverWait
db = pickledb.load('pizza-db.json', False)
driver_path = "./chromedriver"
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
        driver.find_element_by_xpath('//*[@id="start-order-type"]/div[1]/div[2]/button[3]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="start-delivery-address"]').send_keys(db.get('street'))
        driver.find_element_by_xpath('//*[@id="start-delivery-address-line2"]').send_keys(db.get('suburb'))
        driver.find_element_by_xpath('//*[@id="start-delivery-zip"]').send_keys(db.get('postcode'))
        driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[2]/button[1]').click()
        driver.find_element_by_xpath('//*[@id="start-order"]').click()
    except ElementClickInterceptedException:
        print("Exception: " + driver.find_element_by_xpath('//*[@id="start-order-time-info"]/div[3]').text)
        driver.close()
        exit(1)
    time.sleep(5)


def get_order():
    driver.find_element_by_partial_link_text('Meal Combos').click()
    time.sleep(1)
    driver.find_element_by_xpath(meal.ME.value).click()
    add_to_order(pizza.MEATLOVERS)
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
        element = WebDriverWait(driver, 10).until(
            lambda finder: finder.find_element_by_xpath('//*[@id="menu-app"]/div[13]/div/div/form/div[2]/button[3]'))
        element.click()
    except ElementNotInteractableException:
        element = WebDriverWait(driver, 10).until(
            lambda finder: finder.find_element_by_xpath('//*[@id="menu-app"]/div[13]/div/div/form/div[2]/button[1]/span'))
        element.click()


def complete_order():
    driver.find_element_by_xpath('//*[@id="full_name"]').send_keys(db.get("name"))
    driver.find_element_by_xpath('//*[@id="phone"]').send_keys(db.get("phone"))
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(db.get("email"))
    driver.find_element_by_xpath('//*[@id="custom_field_suburb"]').send_keys(db.get("suburb"))
    select_button_by_link_text("No tip")

    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//*[@id="card_number"]').send_keys(db.get("card_number"))
    driver.switch_to.default_content()

    iframe = driver.find_elements_by_tag_name('iframe')[1]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//*[@id="cvv"]').send_keys(db.get("cvv"))
    driver.switch_to.default_content()

    driver.find_element_by_xpath('//*[@id="month"]').send_keys(db.get("exp_month"))
    driver.find_element_by_xpath('//*[@id="year"]').send_keys(db.get("exp_year"))
    #select_button_by_link_text("Submit Order")


def select_button_by_link_text(text):
    element = WebDriverWait(driver, 10).until(
        lambda finder: finder.find_element_by_link_text(text))
    element.click()


driver = webdriver.Chrome(options=option, executable_path=driver_path)
fill_address_details()
get_order()

