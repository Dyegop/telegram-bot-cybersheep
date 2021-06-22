"""
PROJECT - TELEGRAM BOT
-Development of a telegram bot to perform different actions
    *Send weather forecast every day at defined time


NOTES:
-https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.callbackcontext.html
-https://python-telegram-bot.readthedocs.io/en/latest/telegram.update.html
-Telegram API only supports UTF-8, but Python works with Unicode
-Emojis in Unicode begins with U0000 or U0001
"""

# Imports
import time
import json
import handlers
import logging
from telegram.ext import Updater



# Token
token = json.load(open("../data/tokens.json", "r"))["telegramBot"]


# Log
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
# Handler for file log
log_handler = logging.FileHandler(f'../logs/log_filename_{time.strftime("%Y%m%d")}.log', 'w', 'utf-8')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
root_logger.addHandler(log_handler)





# Start the bot
if __name__ == '__main__':
    # Create the Updater and pass it your bot's token
    u = Updater(token)

    # Get the dispatcher to register handlers and register them
    dispatcher = u.dispatcher
    handlers.add_handlers(dispatcher)

    # Schedule permanent jobs
    # job_minute = j.run_repeating(commands.forecast, interval=10, first=10)
    # job_minute.enabled = False  # Temporarily disable this job
    # job_minute.schedule_removal()  # Remove this job completely

    # Start the Bot
    u.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    # This should be used most of the time, since start_polling() is non-blocking and will stop the bot gracefully
    u.idle()
