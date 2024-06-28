import logging
from AP.new import APNew
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions

class AP:
    def __init__(self, CONFIG, CURRENT_DATE):
        self.CONFIG = CONFIG
        self.CURRENT_DATE = CURRENT_DATE
        self.browser = Selenium()
        self.news = []

    def navigate_to_new(self):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        logging.info('Starting web automation process')
        self.browser.open_browser(self.CONFIG.AP.url, options=opts)
        self.browser.wait_until_element_is_visible(self.CONFIG.AP.search_button,
                                        self.CONFIG.delays.medium)
        search_button = self.browser.find_element(self.CONFIG.AP.search_button)
        logging.info('Searching for phrase')
        search_button.click()
        search_bar = self.browser.find_element(self.CONFIG.AP.search_bar)
        search_bar.send_keys(self.CONFIG.phrase)
        self.browser.press_keys(None, 'ENTER')

    def get_news(self):
        self.page_counter = 2
        keep_searching = True
        base_next_url= ''
        while keep_searching:
            self.browser.wait_until_element_is_visible(self.CONFIG.AP.search_results_container,
                                                self.CONFIG.delays.medium)
            search_results = self.browser.find_element(self.CONFIG.AP.search_results_container)
            self.browser.wait_until_element_is_visible(self.CONFIG.AP.search_results,
                                                self.CONFIG.delays.medium)
            self.add_filtered_news(search_results)
            if self.page_counter == 2:
                next = self.browser.find_element(self.CONFIG.AP.next_page_button)
                base_next_url = next.find_element(By.CSS_SELECTOR,
                                                self.CONFIG.first_child).get_attribute('href')
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
            if not self.element_exists(self.CONFIG.AP.logo, self.CONFIG.delays.short):
                logging.warning(f'AP News doesn\'t support more than {self.page_counter - 2} news pages')
                return
            raise(e)
    
    def add_filtered_news(self, search_results):
        for web_new in search_results.find_elements(By.CLASS_NAME, 'PagePromo'):
            try:
                self.news.append(APNew(self.CONFIG, self.CURRENT_DATE,
                                       self.CONFIG.paths.output, web_new).__dict__)
            except Exception as e:
                logging.warning(e)