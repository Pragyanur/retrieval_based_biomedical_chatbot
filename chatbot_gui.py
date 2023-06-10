import tkinter as tk
from chatbot import chat, predict_disease, bot_response
import utility as u


class useful:                                   # static class implemented in order to share the same data throughout the program
    
    disease = "none"
    @staticmethod
    def update_disease(self, x):
        self.disease = x
    
    @staticmethod
    def return_disease(self):
        return self.disease

def intro():
    chat_display.insert(tk.END, "You can search for causes, complications, current research, diagnosis, epidemiology, prevention, prognosis, risk factors, symptoms or treatment of any of the following diseases:\n\n")
    diseases = list(u.view_diseases())
    chat_display.insert(tk.END, diseases)
    chat_display.insert(tk.END, "\n\n\nHow to use:\nTo start a conversation, enter your query in the text-box below and hit 'SEND'\nTo clear the conversation session, hit the 'RESET' button\n\n\n")


def send_message():
    previous_disease = useful.return_disease(useful)
    message = input_text.get("1.0", tk.END).strip()
    if message:
        chat_display.insert(tk.END, "User: " + message + "\n\n")
        curr_d = predict_disease(message, previous_disease)
        useful.update_disease(useful, curr_d)
        response = bot_response(message, curr_d)
        chat_display.insert(tk.END, "Bot: " + response + "\n\n")
    input_text.delete("1.0", tk.END)

def clear_conversation():
    useful.update_disease(useful, "none")                   # update the static variable disease to "none"
    chat_display.delete("1.0", tk.END)
    intro()


root = tk.Tk()
root.title("Bio-medical chatbot")


# Chat display area
chat_display = tk.Text(root, height=20, width=50, padx=5, pady=5 )
chat_display.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Input text area
input_text = tk.Text(root, height=3, width=50, padx=5, pady=5)
input_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# SEND button
send_button = tk.Button(root, text="SEND", command=send_message)
send_button.grid(row=2, column=0, padx=5, pady=5)

# RESET button
clear_button = tk.Button(root, text="RESET", command=clear_conversation)
clear_button.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()