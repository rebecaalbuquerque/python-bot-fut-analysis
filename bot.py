import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re

PORT = int(os.environ.get('PORT', 8443))
ADD_REGEX = "(([01]?[0-9]|2[0-3]):[0-5][0-9]);([0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2});(-?[0-9]{1,2});(.+?);(\\b[^\\d\\W]+\\b$)"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5174025195:AAHCf4_dpbtBNO27mny1ximvYYZtKf6zYw8'

# Setting up google sheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Bot')
sheet_instance = sheet.get_worksheet(0)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def teste(update, context):
    """Echo the user message."""
    update.message.reply_text("\U0001F3C6")


def add(update, context):
    bet_message = update.message.text
    match = re.search(ADD_REGEX, bet_message)

    if match:
        bet = bet_message.split(";")

        championship = bet[4]
        order_result = bet[2]
        order_array = bet[1].split(".")
        bet_type = bet[3]
        order = ""

        for index, value in enumerate(order_array):
            if value == order_result:
                order += "["
                order += value
                order += "]"
            else:
                order += value

            if index < len(order_array) - 1:
                order += "."

        result = "\U00002705" if int(order_result) > -1 else "\U0000274C"

        response = """
        Você salvou a seguinte aposta:
        
        \U0001F3C6 {}
        \U000026BD {}
        \U000023F0 {}
        
        {}
        """.format(championship, bet_type, order, result)
        update.message.reply_text(response)
    else:
        update.message.reply_text("Desculpe, não entendi o comando")

    sheet_instance.insert_row(
        [["00:04", "7.10.13", "7", "over 2.5", "super"], ["00:04", "7.10.13", "7", "over 2.5", "super"]],
        2
    )


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    print("Port: ")
    print(PORT)
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("teste", teste))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url='https://python-bot-fut-analysis.herokuapp.com/' + TOKEN
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
