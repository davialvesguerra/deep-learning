from dotenv import load_dotenv
import os
import logging
import csv
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

RESUME, CONTEXT, SAVE_INFO = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their resume."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Informe o resumo",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return RESUME

async def get_context(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the resume and asks for a context."""
    logger.info("Resume: %s", update.message.text)
    context.user_data['resumo'] = update.message.text

    await update.message.reply_text(
        "Informe o contexto",
        reply_markup=ReplyKeyboardRemove(),
    )

    return CONTEXT

async def save_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    
    context.user_data['contexto'] = update.message.text

    infos = {
        'resumo': context.user_data['resumo'],
        'contexto': context.user_data['contexto']
    }
    arquivo_saida = './dados/infos.csv'
    fieldnames = list(infos.keys())
    with open(arquivo_saida, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows([infos])


    await update.message.reply_text(
        "Bye! Your resume are safe! Keep learning!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("s", start)],
        states={
            RESUME: [MessageHandler(filters.TEXT, get_context)],
            CONTEXT: [MessageHandler(filters.TEXT, save_info)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],

    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()