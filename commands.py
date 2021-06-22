""" COMMANDS MODULE - Register all commands for the bot """

# Imports
import json
import requests
import logging
import datetime
import functions as f
from telegram import Update, error, ParseMode
from telegram.ext import ConversationHandler, CallbackContext



# TODO - Move texts to a list to have them all in one place
# ConversationHandlers variables
LOCATION = range(1)

# Other variables
location = ["40.4165", "-3.70256"]  # default values to Plaza Sol, Madrid





# -------------- COMMANDS START BY THE USER --------------

# Start the bot
def start(update: Update, context: CallbackContext):
    """
        :param update: telegram.Update object
        :param context: telegram.ext.CallbackContext object

        context.bot.send_message()  -> send message to the user
        update.message.reply_text() -> shortcut for context.bot.send_message()
        update.effective_chat.id    -> return current chat_id
    """
    welcome = "Welcome human! \U0001F916 \U0001F411"
    # context.bot.send_message(chat_id=update.effective_chat.id, text=welcome)
    update.message.reply_text(welcome)


# Stop scheduled job
def stop(update: Update, context: CallbackContext):
    """
        Usage: /stop command1 command2
        In order to ease user experience, command that starts a job and the given job must own the same name

        context.job_queue.get_jobs_by_name("job_name") -> get job object by name
        schedule_removal() -> remove scheduled job
    """
    for i in context.args:
        # Get
        job = context.job_queue.get_jobs_by_name(i)
        job[0].schedule_removal()
        update.message.reply_text(f'<b>Command {i} stopped</b>', parse_mode=ParseMode.HTML)


# Return bot version
def botver(update: Update, context: CallbackContext):
    update.message.reply_text("2021-03-08v01-AlphaRelease")


# Cancel command for ConversationHandlers
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Command canceled')
    return ConversationHandler.END


# Start location_handler
def setlocation(update: Update, context: CallbackContext):
    update.message.reply_text('Please, share your current location \U0001F4CD\n'
                              'Send /cancel at any moment to exit')
    return LOCATION


# Activate forecast notification
def forecast(update: Update, context: CallbackContext):
    """
        context.job_queue -> jobQueue asociated with this context
    """
    update.message.reply_text('Forecast notifications activated\n'
                              'A message will be delivered from 09:00 AM every 6 hours')
    # Run every 6h from 09:00:00 AM
    context.job_queue.run_repeating(getForecast, interval=21600, first=datetime.time(9, 0, 0, 0),
                                    context=update.message.chat_id, name="forecast")





# -------------- COMMANDS START BY OTHER COMMANDS --------------

# Get geographical coordinates from user
def getcoordinates(update: Update, context: CallbackContext):
    location[0], location[1] = (update.message.location.latitude, update.message.location.longitude)
    update.message.reply_text('Location has been updated')
    return ConversationHandler.END


# Message current weather for saved location
def getForecast(context, welcome):
    try:
        # Call OpenWeather API
        lat = location[0]
        lon = location[1]
        w, temp, loc = f.openWeatherAPI_call(lat, lon)
        # Send message with results
        context.bot.send_message(chat_id=context.job.context, text=(
            f'{welcome}\n'
            f'{f.getCity(lat, lon)}: {temp["temp"]:.1f}ºC (feels like: {temp["feels_like"]:.1f}ºC)\n'
            f'Max: {temp["temp_max"]:.1f}ºC - Min: {temp["temp_min"]:.1f}ºC\n'
            f'{w["main"]} - {w["description"]} {f.getWeatherEmoji(w["id"]) * 2}')
        )
    except error.BadRequest:
        logging.error("Chat_id is empty")
