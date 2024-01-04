import os
from datetime import timedelta

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import Updater, CommandHandler

from src.bot.commands import start
from src.bot.repeatings import send_emails_data

load_dotenv()


def start_bot():
    bot = Bot(os.getenv('BOT_API_TOKEN'))
    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    job = updater.job_queue

    job.run_repeating(
        send_emails_data,
        interval=timedelta(seconds=100),
        first=1,
    )

    print('Bot started !!!')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_bot()
