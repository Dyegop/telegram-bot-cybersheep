""" HANDLERS MODULE - Register all handlers for the bot """

# Imports
import commands as c
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters



# Variables
LOCATION = range(1)


# CommandHandlers
start_handler = CommandHandler('start', c.start)
stop_handler = CommandHandler('stop', c.stop, pass_args=True)
botver_handler = CommandHandler('botver', c.botver)
forecast_handler = CommandHandler('forecast', c.forecast)


# ConversationHandlers
location_handler = ConversationHandler(
    entry_points=[CommandHandler('setlocation', c.setlocation, Filters.text)],
    states={
        LOCATION: [MessageHandler(Filters.location, c.getcoordinates)],
    },
    fallbacks=[CommandHandler('cancel', c.cancel)]
)


# Register calls in the dispatcher
def add_handlers(dispatcher):
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(stop_handler)
    dispatcher.add_handler(botver_handler)
    dispatcher.add_handler(location_handler)
    dispatcher.add_handler(forecast_handler)