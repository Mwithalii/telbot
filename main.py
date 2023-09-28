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
    await Update.message.reply_text('Hi! \n Welcome to Summarizer Bot. \n 1.To open the summarizer, type out the command /summarizer \n 2.To open the query document, type out the command /query \n 3.To stop chatting, type out the command /exit')

async def summarizer(Update: Update, context: ContextTypes.DEFAULT_TYPE):
   import summarizer

async def query(Update: Update, context: ContextTypes.DEFAULT_TYPE):
   import query_document

async def exit(Update: Update, context: ContextTypes.DEFAULT_TYPE):
   await Update.message.reply_text('Thank you for using Summarizer Bot. \n Have a nice day!')
   

#handle responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hi' in processed:
        return 'Hi! My name is Summarizer Bot. \n I am here to make your work easier by summarizing documents for you and querying documents. \n 1. To open the document summarizer, reply with SUMMARIZE \n 2. To answer queries on a document, reply with QUERY \n 3. To stop chatting, reply with EXIT'
    
    if 'summarize' in processed:
        import summarizer
    
    if 'query' in processed:
        import query_document
    
    if 'exit' in processed:
        return 'Thank you for using Summarizer Bot. \n Have a nice day!'
    
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
    app.add_handler(CommandHandler('summarizer', summarizer))
    app.add_handler(CommandHandler('query', query))
    app.add_handler(CommandHandler('exit', exit))

    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #errors
    app.add_error_handler(error)

    #poll the bot
    print("Polling...")
    app.run_polling(poll_interval=3)