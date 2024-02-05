import datetime as dt

from src.bot.utils import send_emails_data_message
from src.config import (
    EMAIL_DATE_FORMAT,
    SHEET_NAME,
    UID_COLUMN_NAME,
    DATE_COLUMN_NAME,
    ADDRESS_COLUMN_NAME,
    DATA_PATH,
    SENT_EMAILS_UID_FILENAME,
)
from src.email.email_service import EmailClient
from src.google_sheets.sheets import GoogleSheets
from src.utils.csv_handler import CSVHandler
from src.utils.logging_config import logger


def send_emails_data(context):
    email_client = EmailClient()
    csv_handler = CSVHandler(DATA_PATH / SENT_EMAILS_UID_FILENAME)

    if not csv_handler.file_is_exists():
        csv_handler.create_csv(
            [UID_COLUMN_NAME, DATE_COLUMN_NAME, ADDRESS_COLUMN_NAME]
        )

    yesterday_date = (dt.date.today() - dt.timedelta(1)).strftime(
        EMAIL_DATE_FORMAT
    )
    try:
        emails = email_client.fetch_emails(yesterday_date)
    except Exception as error:
        logger.exception('Ошибка получения писем', exc_info=False)
        raise error
    google_sheets = GoogleSheets()
    for email in emails:
        data_to_sheets = [
            email.name,
            email.address,
            email.date,
            email.subject,
        ]
        try:
            google_sheets.update_values(data_to_sheets, f'{SHEET_NAME}!A:D')
        except Exception as error:
            logger.exception(
                f'Ошибка отправки в Google Sheets {data_to_sheets}',
                exc_info=False,
            )
            raise error
        try:
            send_emails_data_message(context, email)
        except Exception as error:
            logger.exception(
                f'Ошибка отправки в телеграм {email}', exc_info=False
            )
            raise error
        csv_handler.update_rows([email.uid, email.date, email.address])
        logger.info(f'Отправлено письмо в гугл и тг {email}')
