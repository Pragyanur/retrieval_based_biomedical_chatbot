import chatbot as CB
        
def chat():
    msg = "hello"
    while msg.lower() != "exit":
        msg = str(input("User: "))
        print("Bot: ", CB.response(msg))

chat()