import re
import logging
import requests

def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error downloading the image: {e}")

def clean_filename(filename, replace_char='_'):
    invalid_chars = r'[<>:"/\\|?*]'
    cleaned_filename = re.sub(invalid_chars, replace_char, filename)
    return cleaned_filename

def first_date_of_month(date):
    return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)