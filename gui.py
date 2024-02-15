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

if __name__ == "__main__":
    browse_pdf_file()
