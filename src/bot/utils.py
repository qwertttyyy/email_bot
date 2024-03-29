from telegram.error import Unauthorized

from src.bot.templates import EMAIL_DATA_MESSAGE
from src.config import DATA_PATH, USERS_DATA_FILENAME, CHAT_ID_COLUMN_NAME
from src.email.email_service import Email
from src.utils.csv_handler import CSVHandler


def send_emails_data_message(context, email_data: Email):
    message = EMAIL_DATA_MESSAGE.format(
        name=email_data.name,
        address=email_data.address,
        date=email_data.date,
        subject=email_data.subject,
    )
    csv_handler = CSVHandler(DATA_PATH / USERS_DATA_FILENAME)
    if csv_handler.file_is_exists():
        chat_ids = csv_handler.read_column(CHAT_ID_COLUMN_NAME)
        for chat_id in chat_ids:
            try:
                context.bot.send_message(
                    chat_id=chat_id, text=message, parse_mode='html'
                )
            except Unauthorized:
                csv_handler.remove_row_by_column_value(
                    CHAT_ID_COLUMN_NAME, chat_id
                )
