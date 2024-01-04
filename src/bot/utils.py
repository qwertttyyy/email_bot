from src.bot.templates import EMAIL_DATA_MESSAGE
from src.config import DATA_PATH, USERS_DATA_FILENAME
from src.email.email_service import Email
from src.state_manager import StateManager


def send_emails_data_message(context, email_data: Email):
    message = EMAIL_DATA_MESSAGE.format(
        name=email_data.name,
        address=email_data.address,
        date=email_data.date,
        subject=email_data.subject,
    )
    state_manager = StateManager(DATA_PATH / USERS_DATA_FILENAME)
    if state_manager.file_is_exists():
        chat_ids = state_manager.read_row('Chat_id')
        for chat_id in chat_ids:
            context.bot.send_message(
                chat_id=chat_id, text=message, parse_mode='html'
            )
