import os
import logging
import pandas as pd
from datetime import datetime
from utils.config import load_config

if __name__ == '__main__':
    CONFIG = load_config('config.yaml')
    CURRENT_DATE = datetime.today()
    CURRENT_DATE_FOLDER = f'{CONFIG.paths.output}/{CURRENT_DATE:%m_%d_%Y %H-%M-%S}'
    from AP.process import AP
    os.mkdir(CURRENT_DATE_FOLDER)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    retries = 0
    while retries < CONFIG.max_retries:
        try:
            ap_process = AP()
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