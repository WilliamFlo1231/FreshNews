import re
from datetime import datetime
from selenium.webdriver.common.by import By
from __main__ import CONFIG, CURRENT_DATE_FOLDER
from selenium.common.exceptions import NoSuchElementException
from utils.helper_functions import download_image, clean_filename

class APNew:
    def __init__(self, search_phrase, web_new) -> None:
        self.title = web_new.find_element(By.CLASS_NAME, CONFIG.new.title).text
        self.description = web_new.find_element(By.CLASS_NAME, CONFIG.new.description).text
        date_container = web_new.find_element(By.CLASS_NAME, CONFIG.new.date_container)
        unix_timestamp = date_container.find_element(By.CSS_SELECTOR,
                                                     CONFIG.first_child).get_attribute(CONFIG.new.timestamp)
        self.date = datetime.fromtimestamp(int(unix_timestamp) / 1000)
        amount_matches = re.findall(CONFIG.new.money_amount_regex,
                                    f'{self.title} {self.description}')
        self.has_money_amount = bool(amount_matches)
        try:
            web_picture = web_new.find_element(By.CLASS_NAME, CONFIG.new.image)
            picture_url = web_picture.get_attribute('src')
            download_image(picture_url, f'{CURRENT_DATE_FOLDER}/{clean_filename(self.title)}.jpg')
        except NoSuchElementException:
            self.picture = None