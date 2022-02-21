import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re

PORT = int(os.environ.get('PORT', 8443))
ADD_REGEX = "(([01]?[0-9]|2[0-3]):[0-5][0-9]);([0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2});([0-9]{1,2});(r|g);(.+?);(\\b[^\\d\\W]+\\b$)"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5174025195:AAHCf4_dpbtBNO27mny1ximvYYZtKf6zYw8'


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


def add(update, context):
    bet_message = update.message.text
    match = re.search(ADD_REGEX, bet_message)

    if match:
        bet = bet_message.split(";")
        response = """
        Você salvou a seguinte aposta:
        
        {}
        {}
        {}
        """.format(bet[5], bet[1], bet[3])
        update.message.reply_text(response)
    else:
        update.message.reply_text("Desculpe, não entendi o comando")


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
