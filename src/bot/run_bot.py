import os
from datetime import timedelta

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, CommandHandler

from src.bot.commands import start
from src.bot.repeatings import send_emails_data
from src.config import (
    FIRST_REQUEST_DELAY_SECONDS,
    EMAIL_CHECK_INTERVAL,
)

load_dotenv()


def start_bot():
    bot = Bot(os.getenv('BOT_API_TOKEN'))
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher

    job = updater.job_queue

    job.run_repeating(
        send_emails_data,
        interval=timedelta(seconds=int(EMAIL_CHECK_INTERVAL)),
        first=int(FIRST_REQUEST_DELAY_SECONDS),
    )

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_bot()
