import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATE_FORMAT = '%d.%m.%Y'
EMAIL_DATE_FORMAT = '%d-%b-%Y'

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'src' / 'data'
SENT_EMAILS_UID_FILENAME = 'sent_email_uid.csv'
USERS_DATA_FILENAME = 'users_data.csv'

SHEET_NAME = os.getenv('SHEET_NAME')

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

MAX_LOG_FILE_SIZE = 50 * 1024

FIRST_REQUEST_DELAY_SECONDS = os.getenv('FIRST_REQUEST_DELAY_SECONDS')
EMAIL_CHECK_INTERVAL = os.getenv('EMAIL_CHECK_INTERVAL')


UID_COLUMN_NAME = 'UID'
DATE_COLUMN_NAME = 'Дата'
ADDRESS_COLUMN_NAME = 'Адрес'
CHAT_ID_COLUMN_NAME = 'ChatId'
