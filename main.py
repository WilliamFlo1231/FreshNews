import os
from AP.new import APNew
from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By

browser = Selenium()

browser.open_browser('https://apnews.com/', service_log_path=os.path.devnull)

browser.wait_until_element_is_visible('//*[@class="SearchOverlay-search-button"]')

search_button = browser.find_element('//*[@class="SearchOverlay-search-button"]')

search_button.click()

search_bar = browser.find_element('//*[@class="SearchOverlay-search-input"]')

search_bar.send_keys('Trump fans.')

browser.press_keys(None, 'ENTER')

page_counter = 2
keep_searching = True
base_next_url= ''

while keep_searching:
    browser.wait_until_element_is_visible('//*[@class="SearchResultsModule-results"]', 15)
    search_results = browser.find_element('//*[@class="SearchResultsModule-results"]')
    browser.wait_until_element_is_visible('//*[@class="PagePromo"]', 15)
    news = [APNew(new) for new in search_results.find_elements(By.CLASS_NAME, 'PagePromo')]
    if page_counter == 2:
        next = browser.find_element('//*[@class="Pagination-nextPage"]')
        base_next_url = next.find_element(By.CSS_SELECTOR, ':first-child').get_attribute('href')
    browser.go_to(f'{base_next_url[:-1]}{page_counter}')
    page_counter += 1
...