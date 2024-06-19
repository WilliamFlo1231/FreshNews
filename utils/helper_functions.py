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
