from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

class Browser():

    def __init__(self, headless=False):
        chrome_options = Options()
        chrome_options.headless = headless
        self.browser = webdriver.Chrome(options=chrome_options)

    def load_page(self, url):
        self.browser.maximize_window()
        time.sleep(2)
        self.browser.get(url)
        time.sleep(2)

    def get_elements_by_css(self, selector):
        try:
            element = self.browser.find_elements(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            print(f'Selecter {selector} not found')
            element = None
        return element

    def get_element_by_css(self, selector):
        try:
            element = self.browser.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            print(f'Selecter {selector} not found')
            element = None
        return element

    def get_sub_elements_by_css(self, element, selector):
        try:
            element = element.find_elements(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            print(f'Selecter {selector} not found')
            element = None
        return element

    def get_sub_element_by_css(self, element, selector):
        try:
            element = element.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            print(f'Selecter {selector} not found')
            element = None
        return element

    def get_element_text(self, element):
        return 'N/A' if element is None else element.text

    def scroll_down(self, scrolls):
        body = self.browser.find_element(By.CSS_SELECTOR, 'body') 
        for i in range(scrolls):
            body.send_keys(Keys.PAGE_DOWN)

    def quit(self):
        self.browser.quit()