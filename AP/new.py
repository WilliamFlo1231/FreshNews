import re
from datetime import datetime
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta
from selenium.common.exceptions import NoSuchElementException
from utils.helper_functions import download_image, clean_filename, first_date_of_month

class OlderNewException(Exception):
    def __init__(self, message='New is not within allowed date range.'):
        self.message = message
        super().__init__(self.message)


class APNew:
    def __init__(self, CONFIG, CURRENT_DATE, CURRENT_DATE_FOLDER, web_new) -> None:
        months_to_review = 0 if CONFIG.months_to_review <= 1 else -(CONFIG.months_to_review - 1)
        self.title = web_new.find_element(By.CLASS_NAME, CONFIG.new.title).text
        try:
            self.description = web_new.find_element(By.CLASS_NAME, CONFIG.new.description).text
        except NoSuchElementException:
            self.description = 'No Description'
        title_description = f'{self.title} {self.description}'
        date_container = web_new.find_element(By.CLASS_NAME, CONFIG.new.date_container)
        unix_timestamp = date_container.find_element(By.CSS_SELECTOR,
                                                     CONFIG.first_child).get_attribute(CONFIG.new.timestamp)
        self.date = datetime.fromtimestamp(int(unix_timestamp) / 1000)
        oldest_date = first_date_of_month(CURRENT_DATE + relativedelta(months=months_to_review))
        if self.date <= oldest_date:
            raise OlderNewException
        amount_matches = re.findall(CONFIG.new.money_amount_regex,
                                    title_description)
        
        self.has_money_amount = bool(amount_matches)
        self.phrase_count = len(re.findall(CONFIG.phrase.lower(),
                                           title_description.lower()))
        try:
            web_picture = web_new.find_element(By.CLASS_NAME, CONFIG.new.image)
            picture_url = web_picture.get_attribute('src')
            self.picture = f'{CURRENT_DATE_FOLDER}/{clean_filename(self.title)}.jpg'
            download_image(picture_url, self.picture)
        except NoSuchElementException:
            self.picture = 'No Picture'