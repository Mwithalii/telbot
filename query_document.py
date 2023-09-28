import tkinter as tk
from tkinter import filedialog
import openai
import dotenv
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("AI_API_KEY")
openai.api_key = api_key

# Function to process the user's question and document
# ...

# Function to process the user's question and document
def answer_question():
    question = question_entry.get()
    document_path = document_path_label.cget("text")
    
    if not question or not document_path:
        answer_label.config(text="Please provide a question and upload a document.")
        return
    
    try:
        with open(document_path, "r", encoding="utf-8", errors="replace") as file:
            document = file.read()
        
        # Truncate the document to fit within the maximum context length
        max_context_length = 4097 - len(f"Document: {document}\nQuestion: {question}\nAnswer: ")
        if len(document) > max_context_length:
            document = document[:max_context_length]
        
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Document: {document}\nQuestion: {question}\nAnswer:",
            max_tokens=50,
        )
        
        answer = response.choices[0].text
        answer_label.config(text=f"Answer: {answer}")
    except Exception as e:
        answer_label.config(text=f"An error occurred: {str(e)}")


# Function to handle document upload
def upload_document():
    file_path = filedialog.askopenfilename()
    
    if file_path:
        document_path_label.config(text=file_path)

# Create the main tkinter window
window = tk.Tk()
window.title("OpenAI Question Answering App")

# Create widgets
question_label = tk.Label(window, text="Enter your question:")
question_entry = tk.Entry(window, width=50)
document_button = tk.Button(window, text="Upload Document", command=upload_document)
document_path_label = tk.Label(window, text="")
answer_button = tk.Button(window, text="Get Answer", command=answer_question)
answer_label = tk.Label(window, text="")

# Arrange widgets in the window
question_label.pack()
question_entry.pack()
document_button.pack()
document_path_label.pack()
answer_button.pack()
answer_label.pack()

# Start the tkinter main loop
window.mainloop()
