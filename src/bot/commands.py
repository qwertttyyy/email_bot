from src.config import DATA_PATH, USERS_DATA_FILENAME, CHAT_ID_COLUMN_NAME
from src.utils.csv_handler import CSVHandler


def start(update, context):
    chat_id = update.effective_chat.id
    csv_handler = CSVHandler(DATA_PATH / USERS_DATA_FILENAME)

    if not csv_handler.file_is_exists():
        csv_handler.create_csv([CHAT_ID_COLUMN_NAME])

    existing_chat_ids = csv_handler.read_column(CHAT_ID_COLUMN_NAME)

    if str(chat_id) not in existing_chat_ids:
        csv_handler.update_rows([chat_id])

    context.bot.send_message(
        chat_id=chat_id, text='Бот запущен и готов к работе!'
    )
