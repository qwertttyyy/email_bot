import logging
import os
from logging.handlers import RotatingFileHandler

from src.config import DATA_PATH, MAX_LOG_FILE_SIZE

level = logging.INFO
logs_format = '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
formatter = logging.Formatter(logs_format)

log_file_path = os.path.join(DATA_PATH, 'logs.log')
file_handler = RotatingFileHandler(
    log_file_path,
    mode='a',
    maxBytes=MAX_LOG_FILE_SIZE,
    encoding='UTF-8',
)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(level)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
