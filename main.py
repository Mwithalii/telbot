import telegram
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
TOKEN: Final = api_key
BOT_USERNAME: Final = '@otpverifierBot'

#commands
async def start_command(Update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Update.message.reply_text('Hi! Welcome to OTP Verifier Bot.')

async def help_command(Update: Update, context: ContextTypes.DEFAULT_TYPE):
    await Update.message.reply_text('Hi! I am an OTP Verifier Bot. I can verify OTPs for you.')

#handle responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hi!'
    
    if 'how are you' in processed:
        return 'I am fine. How are you?'
    
    if 'fine' in processed:
        return 'Nice to hear that.'
    
    return 'Sorry, I don\'t understand you.'

async def handle_message(Update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = Update.message.chat.type
    text: str = Update.message.text

    print(f'User ({Update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await Update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_error_handler(error)

    #poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)