import logging
import pandas as pd
from AP.process import AP
from datetime import datetime
from robocorp.tasks import task
from utils.config import load_config

@task
def main():
    CONFIG = load_config('config.yaml')
    CURRENT_DATE = datetime.today()
    CURRENT_DATE_FOLDER = f'{CONFIG.paths.output}'
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    retries = 0
    while retries < CONFIG.max_retries:
        try:
            ap_process = AP(CONFIG, CURRENT_DATE, CURRENT_DATE_FOLDER)
            ap_process.start()
            logging.info('Saving News Report')
            output_data = pd.DataFrame(ap_process.news)
            output_data['date'] = output_data['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            output_data.to_excel(f'{CURRENT_DATE_FOLDER}/{CONFIG.phrase}.xlsx', index=False)
            break
        except Exception as e:
            logging.error(e)
            retries += 1
    ...