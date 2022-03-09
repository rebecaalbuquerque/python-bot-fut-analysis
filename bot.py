import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

from bet_formater import get_bet
from google_sheets_export import register_bet
from telegram_chat_data_export import export_telegram_chat_bet

PORT = int(os.environ.get('PORT', 8443))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5174025195:AAHCf4_dpbtBNO27mny1ximvYYZtKf6zYw8'


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def add(update, context):
    bet_message = update.message.text
    result = get_bet(bet_message)

    if result["success"]:
        print(
            result["bet"]["time"],
            result["bet"]["order"],
            result["bet"]["order_result"],
            result["bet"]["bet_type"],
            result["bet"]["championship"]
        )
        register_bet(
            result["bet"]["time"],
            result["bet"]["order"],
            result["bet"]["order_result"],
            result["bet"]["bet_type"],
            result["bet"]["championship"]
        )
        update.message.reply_text(result["message"])
    else:
        update.message.reply_text(result["message"])


def add_file(update, context):
    print("add_file")
    file = context.bot.get_file(update.message.document).download()
    print(file)
    print(type(file))
    bet_list = export_telegram_chat_bet(file)

    for bet in bet_list:
        result = get_bet(bet)

        if result["success"]:
            register_bet(
                result["bet"]["time"],
                result["bet"]["order"],
                result["bet"]["order_result"],
                result["bet"]["bet_type"],
                result["bet"]["championship"]
            )
        else:
            print("deu ruim")

    update.message.reply_text(type(file))


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
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(MessageHandler(Filters.document, add_file))

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
