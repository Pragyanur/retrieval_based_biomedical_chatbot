import random
import json
import pickle
import spacy
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import utility as u


lemmatizer = WordNetLemmatizer()

nlp = spacy.load("en_core_sci_sm")
model = load_model("models/intent_classification.h5", compile=False)

responses_starts = open("data/responses.json", "r", encoding="UTF-8")
responses = json.load(responses_starts)

words = pickle.load(open("data/words.pkl", "rb"))
diseases = pickle.load(open("data/diseases.pkl", "rb"))
classes = pickle.load(open("data/classes.pkl", "rb"))
# ignore_words = pickle.load(open("data/ignore_words.pkl", "rb"))
ignore_words = ["?", "!", "XXXX", "disease"]


def predict_disease(msg, prev_disease):
    no_data = False
    doc = nlp(msg)
    entities = list(ent.text for ent in doc.ents)
    for e in entities:
        if e in diseases:
            no_data = False
            prev_disease = e
            return e
        elif e in classes and prev_disease not in diseases:
            no_data = True                                   # debugged
    if no_data:
        prev_disease = "none"
        return "none"
    return prev_disease

# print(diseases, predict_disease("hello lung cancer", "none"))

def bot_response(msg, disease):  # use this function to retrieve response for the user_input
    retrieved_res = "Sorry! I don't understand"  # default if all else fails

    msg_words = nltk.word_tokenize(msg)
    msg_words = [
        lemmatizer.lemmatize(w.lower()) for w in msg_words if w not in ignore_words
    ]

    bag = []
    for word in words:
        if word in msg_words:
            bag.append(1)
        else:
            bag.append(0)

    # Using the model
    # To find the class with highest probability, sorting is done
    prediction = model.predict(np.array([bag]), verbose=False)[0]
    # >>> prediction = [a1 a2 a3 a4 a5 a6....an]----------------------------to_list-
    #                                                                               |
    error_threshold = 0.25  #                                                       v
    results = []

    results = [[i, r] for i, r in enumerate(prediction) if r > error_threshold]
    # >>> results = [[0, p0], [1, p1], ... [n, p(n-1)]]

    results.sort(key=lambda x: x[1], reverse=True)
    # "key=lambda x: x[1]" is a lambda function
    # key -> [lambda[for all tuples 'x' select it's second element]]
    # reverse the order => descending order

    return_list = []  # to store hash value pair lists

    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        # Hash table or dictionary with key: value pairs ["intent": "tag", "probability": pn]
    intent_tag = str(return_list[0]["intent"])
    # print("Type of: intent_tag = ", intent_tag, " ", type(intent_tag))
    # [0] means the first element in the list and
    # ["intent"] gives the value associated with the key "intent"
    # returns intent with highest probability

    all_disease = responses["responses"]

    print("[ looking for: ", intent_tag, "| disease: ", disease, "]")

    # if "tag" matches the predicted disease then choose any of the random responses
    for item in all_disease:
        if disease in item["tag"]:
            retrieved_res = random.choice(item[intent_tag])
            return retrieved_res
    return retrieved_res

def chat():
    disease = "none"    # to keep track of the accessed disease
    print("Welcome to biomedical chatbot demo:\n\n------START CONVERSATION------\n")
    print("Bot: \"You can search for causes, complications, current research, \n\tdiagnosis, epidemiology, prevention, prognosis, risk factors, \n\tsymptoms or treatment of any of the following diseases:\"")
    u.view_diseases()
    while True:
        msg = str(input("User: "))
        if msg.lower() == "exit" or msg.lower() == "quit":
            exit()
        disease = predict_disease(msg, disease)                     # predict disease
        print("Bot: ", bot_response(msg, disease), "\n")            # pass it to response function

chat()