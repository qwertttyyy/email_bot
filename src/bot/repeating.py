import datetime as dt

from src.bot.utils import send_emails_data_message
from src.config import (
    SENT_EMAILS_UID_FILENAME,
    DATA_PATH,
    EMAIL_DATE_FORMAT,
    SHEET_NAME,
    ADMIN_CHAT_ID,
)
from src.email.email_service import EmailClient
from src.google_sheets.sheets import GoogleSheets
from src.state_manager import StateManager
from src.utils.logging_config import logger


def send_emails_data(context):
    state_manager = StateManager(DATA_PATH / SENT_EMAILS_UID_FILENAME)

    if not state_manager.file_is_exists():
        state_manager.create_csv(['UID', 'Дата', 'Адрес'])

    email_client = EmailClient()
    yesterday_date = (dt.date.today() - dt.timedelta(1)).strftime(
        EMAIL_DATE_FORMAT
    )
    try:
        emails = email_client.fetch_emails(yesterday_date)
    except Exception:
        logger.exception('Ошибка получения писем')
        raise Exception()

    google_sheets = GoogleSheets()
    uids = state_manager.read_row('UID')
    for email in emails:
        if email.uid not in uids:
            data_to_sheets = [
                email.name,
                email.address,
                email.date,
                email.subject,
            ]
            try:
                google_sheets.update_values(
                    data_to_sheets, f'{SHEET_NAME}!A:D'
                )
            except Exception:
                logger.exception(
                    f'Ошибка отправки в Google Sheets {data_to_sheets}'
                )
                raise Exception()
            try:
                send_emails_data_message(context, email)
            except Exception:
                logger.exception(f'Ошибка отправки в телеграм {email}')
                raise Exception()
            state_manager.update_rows([email.uid, email.date, email.address])
