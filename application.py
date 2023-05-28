import chatbot as CB
import utility as u


def chat():
    disease = "none"    # to keep track of the accessed disease
    print("Welcome to biomedical chatbot demo:\n\n------START CONVERSATION------\n")
    print("Bot: \"You can search for causes, complications, current research, \n\tdiagnosis, epidemiology, prevention, prognosis, risk factors, \n\tsymptoms or treatment of any of the following diseases:\"")
    u.view_diseases()
    while True:
        msg = str(input("User: "))
        if msg.lower() == "exit" or msg.lower() == "quit":
            exit()
        disease = CB.predict_disease(msg, disease)              # predict disease
        print("Bot: ", CB.response(msg, disease), "\n")         # pass it to response function

chat()