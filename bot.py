import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import time 
import pandas as pd
import csv
import random
from importlib import reload

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.chat_data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"I'm a bot, please talk to me! {context.args[1]}"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    await context.bot.send_photo(update.effective_chat.id,photo='https://thispersondoesnotexist.com/')

async def save_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{update.message.text}'
    )



def main():
    """Função principal que define o bot."""
    # Token fornecido pelo BotFather
    TOKEN = TELEGRAM_API_KEY

    # Obter o dispatcher para registrar os manipuladores
    application = ApplicationBuilder().token(TOKEN).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    echo_handler = CommandHandler('echo', echo)

    save_resume_handler = CommandHandler('s', save_resume)
    save_resume_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), save_resume)

    # Diferentes manipuladores para diferentes comandos
    application.add_handler(echo_handler)
    application.add_handler(save_resume_handler)

    application.run_polling()
    
if __name__ == '__main__':
    main()
