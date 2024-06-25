import os
import logging
from AP.new import APNew
from __main__ import CONFIG
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By

class AP:
    def __init__(self):
        self.browser = Selenium()
        self.news = []

    def navigate_to_new(self):
        logging.info('Starting web automation process')
        self.browser.open_browser(CONFIG.AP.url, service_log_path=os.path.devnull)
        self.browser.wait_until_element_is_visible(CONFIG.AP.search_button,
                                        CONFIG.delays.medium)
        search_button = self.browser.find_element(CONFIG.AP.search_button)
        logging.info('Searching for phrase')
        search_button.click()
        search_bar = self.browser.find_element(CONFIG.AP.search_bar)
        search_bar.send_keys(CONFIG.phrase)
        self.browser.press_keys(None, 'ENTER')

    def get_news(self):
        self.page_counter = 2
        keep_searching = True
        base_next_url= ''
        while keep_searching:
            self.browser.wait_until_element_is_visible(CONFIG.AP.search_results_container,
                                                CONFIG.delays.medium)
            search_results = self.browser.find_element(CONFIG.AP.search_results_container)
            self.browser.wait_until_element_is_visible(CONFIG.AP.search_results,
                                                CONFIG.delays.medium)
            self.add_filtered_news(search_results)
            if self.page_counter == 2:
                next = self.browser.find_element(CONFIG.AP.next_page_button)
                base_next_url = next.find_element(By.CSS_SELECTOR,
                                                CONFIG.first_child).get_attribute('href')
            self.browser.go_to(f'{base_next_url[:-1]}{self.page_counter}')
            self.page_counter += 1

    def element_exists(self, element, timeout=10):
        try:
            self.browser.wait_until_element_is_visible(element, timeout)
            return True
        except:
            return False

    def start(self):
        self.navigate_to_new()
        try:
            self.get_news()
        except AssertionError as e:
            if not self.element_exists(CONFIG.AP.logo, CONFIG.delays.short):
                logging.warning(f'AP News doesn\'t support more than {self.page_counter - 2} news pages')
                return
            raise(e)
    
    def add_filtered_news(self, search_results):
        for web_new in search_results.find_elements(By.CLASS_NAME, 'PagePromo'):
            try:
                self.news.append(APNew(web_new).__dict__)
            except Exception as e:
                logging.warning(e)