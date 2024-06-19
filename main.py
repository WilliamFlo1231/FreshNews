import os
import logging
from datetime import datetime
from utils.config import load_config
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    CONFIG = load_config('config.yaml')
    CURRENT_DATE = datetime.today()
    CURRENT_DATE_FOLDER = f'{CONFIG.paths.output}/{CURRENT_DATE:%m_%d_%Y %H-%M-%S}'
    phrase = 'Tesla'

    from AP.new import APNew

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')

    browser = Selenium()
    os.mkdir(CURRENT_DATE_FOLDER)
    logging.info('Starting the browser')
    browser.open_browser(CONFIG.AP.url, service_log_path=os.path.devnull)
    browser.wait_until_element_is_visible(CONFIG.AP.search_button,
                                        CONFIG.delays.medium)
    search_button = browser.find_element(CONFIG.AP.search_button)
    logging.info('Searching for phrase')
    search_button.click()
    search_bar = browser.find_element(CONFIG.AP.search_bar)
    search_bar.send_keys(phrase)
    browser.press_keys(None, 'ENTER')

    page_counter = 2
    keep_searching = True
    base_next_url= ''

    while keep_searching:
        browser.wait_until_element_is_visible(CONFIG.AP.search_results_container, 15)
        search_results = browser.find_element(CONFIG.AP.search_results_container)
        browser.wait_until_element_is_visible(CONFIG.AP.search_results, 15)
        news = [APNew(phrase, new) for new in
                search_results.find_elements(By.CLASS_NAME, 'PagePromo')]
        if page_counter == 2:
            next = browser.find_element(CONFIG.AP.next_page_button)
            base_next_url = next.find_element(By.CSS_SELECTOR,
                                            CONFIG.first_child).get_attribute('href')
        browser.go_to(f'{base_next_url[:-1]}{page_counter}')
        page_counter += 1
    ...