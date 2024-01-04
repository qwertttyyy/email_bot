from src.config import DATA_PATH, USERS_DATA_FILENAME
from src.state_manager import StateManager


def start(update, context):
    chat_id = update.effective_chat.id
    state_manager = StateManager(DATA_PATH / USERS_DATA_FILENAME)

    if not state_manager.file_is_exists():
        state_manager.create_csv(['Chat_id'])

    existing_chat_ids = state_manager.read_row('Chat_id')

    if str(chat_id) not in existing_chat_ids:
        state_manager.update_rows([chat_id])

    context.bot.send_message(
        chat_id=chat_id, text='Бот запущен и готов к работе!'
    )
