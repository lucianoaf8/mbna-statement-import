import logging
import os
from datetime import datetime

def get_logger(name):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    today = datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(log_dir, f'insert_transactions_{today}.log')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
