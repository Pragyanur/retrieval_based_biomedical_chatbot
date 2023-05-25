import chatbot as CB
   
def chat():
    choice = "none"
    msg = "hello"
    while True:
        msg = str(input("User: "))
        if msg.lower() == "exit" or msg.lower() == "quit":
            exit()
        print("Bot: ", CB.response(msg, choice))

chat()