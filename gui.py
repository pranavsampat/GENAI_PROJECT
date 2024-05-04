import tkinter as tk
from tkinter import scrolledtext
from working_code import execute_intent

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot")

        self.label = tk.Label(master, text="User Input:")
        self.label.pack()

        self.input_entry = tk.Entry(master, width=50)
        self.input_entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

        self.output_text = scrolledtext.ScrolledText(master, width=60, height=20)
        self.output_text.pack()

    def submit(self):
        user_input = self.input_entry.get()
        if user_input:
            self.output_text.insert(tk.END, f"User: {user_input}\n")

            # Pass user input to the main program logic
            response = execute_intent(user_input, 'en')

            self.output_text.insert(tk.END, f"Bot: {response}\n")
            self.output_text.see(tk.END)  # Scroll to the bottom of the text area
            self.input_entry.delete(0, tk.END)  # Clear the input field

root = tk.Tk()
gui = ChatGUI(root)
root.mainloop()  # Add mainloop() here
