import chatbot as CB
   
def chat():
    choice = "none"
    msg = "hello"
    while True:
        msg = str(input("User: "))
        if msg.lower() == "exit" or msg.lower() == "quit":
            exit()
        choice = CB.predict_disease(msg, choice)
        print("Bot: ", CB.response(msg, choice))
        print("\n")

chat()