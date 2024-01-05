import datetime as dt

from src.bot.utils import send_emails_data_message
from src.config import (
    SENT_EMAILS_UID_FILENAME,
    DATA_PATH,
    EMAIL_DATE_FORMAT,
    SHEET_NAME,
    UID_COLUMN_NAME,
    DATE_COLUMN_NAME,
    ADDRESS_COLUMN_NAME,
)
from src.email.email_service import EmailClient
from src.google_sheets.sheets import GoogleSheets
from src.utils.csv_handler import CSVHandler
from src.utils.logging_config import logger


def send_emails_data(context):
    csv_handler = CSVHandler(DATA_PATH / SENT_EMAILS_UID_FILENAME)

    if not csv_handler.file_is_exists():
        csv_handler.create_csv(
            [UID_COLUMN_NAME, DATE_COLUMN_NAME, ADDRESS_COLUMN_NAME]
        )

    email_client = EmailClient()
    yesterday_date = (dt.date.today() - dt.timedelta(1)).strftime(
        EMAIL_DATE_FORMAT
    )
    try:
        emails = email_client.fetch_emails(yesterday_date)
    except Exception as error:
        logger.exception('Ошибка получения писем')
        raise error
    google_sheets = GoogleSheets()
    uids = csv_handler.read_column(UID_COLUMN_NAME)
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
            except Exception as error:
                logger.exception(
                    f'Ошибка отправки в Google Sheets {data_to_sheets}'
                )
                raise error
            try:
                send_emails_data_message(context, email)
            except Exception as error:
                logger.exception(f'Ошибка отправки в телеграм {email}')
                raise error
            csv_handler.update_rows([email.uid, email.date, email.address])
            logger.info(f'Отправлено письмо {email}')
