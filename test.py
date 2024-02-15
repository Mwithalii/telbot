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


##########################################################

""" def extract_text(filepath, progress_var):
    # Open the PDF file in read-binary mode
    with open(filepath, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create an empty string to store the text
        text = ''

        # Loop through each page in the PDF file
        for page_num in range(len(pdf_reader.pages)):
            # Update the progress bar
            progress_var.set(page_num + 1)
            root.update_idletasks()
            root.update()

            # Get the page object
            page_obj = pdf_reader.pages[page_num]

            # Extract the text from the page
            page_text = page_obj.extract_text()

            # Add the text to the string
            text += page_text

    return text """


""" def generate_summary(text, status_var):
    status_var.set('Generating summary...')
    words = text.split()
    max_words = 1000
    prompt = " ".join(words[:max_words])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize this: {prompt}",
        temperature=0.9,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text
    status_var.set('Summary generated')
    progress_var.set(100)
    return summary """


""" def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath.endswith('.pdf'):
        file_path_var.set(filepath)
        output_text.delete(1.0, tk.END)
    else:
        messagebox.showerror(title='Error', message='Please select a PDF file.') """


""" def clear_output():
    output_text.delete(1.0, tk.END) """


""" def copy_to_clipboard():
    pyperclip.copy(output_text.get(1.0, tk.END)) """


""" def save_summary():
    filepath = filedialog.asksaveasfilename(defaultextension='.txt')
    with open(filepath, 'w') as f:
        f.write(output_text.get(1.0, tk.END)) """


""" def summarize():
    filepath = file_path_var.get()
    if filepath:
        progress_var.set(0)
        pdf_text = extract_text(filepath, progress_var)
        summary = generate_summary(pdf_text, status_var)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, summary)
    else:
        messagebox.showerror(title='Error', message='Please select a PDF file.') """


import tkinter as tk
from tkinter import filedialog

def browse_pdf_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Select a PDF file"
    )

    if file_path:
        print("Selected PDF file:", file_path)
        # You can replace the print statement with any code to handle the selected file.
    else:
        print("No file selected.")

##########################################################


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
        return
    
    if 'query' in processed:
        import query_document
        return
    
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