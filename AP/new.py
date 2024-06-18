from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class APNew:
    def __init__(self, web_new) -> None:
        try:
            self.picture = web_new.find_element(By.CLASS_NAME, 'Image')
        except NoSuchElementException:
            self.picture = None
        self.title = web_new.find_element(By.CLASS_NAME, 'PagePromo-title').text
        self.description = web_new.find_element(By.CLASS_NAME, 'PagePromo-description').text
        date_container = web_new.find_element(By.CLASS_NAME, 'PagePromo-date')
        unix_timestamp = date_container.find_element(By.CSS_SELECTOR, ':first-child').get_attribute('data-timestamp')
        self.date = datetime.fromtimestamp(int(unix_timestamp) / 1000)