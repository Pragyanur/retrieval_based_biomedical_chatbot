import random
import json
import pickle
import spacy
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

nlp = spacy.load("en_core_sci_sm")
model = load_model("intent_classification.h5", compile=False)

responses = open("responses.json", "r", encoding="UTF-8")
responses = json.load(responses)

words = pickle.load(open("pickles/words.pkl", "rb"))
diseases = pickle.load(open("pickles/diseases.pkl", "rb"))
classes = pickle.load(open("pickles/classes.pkl", "rb"))

# this will work as a memory to keep the last mentioned disease selected
selected_disease = "none"

def predict_disease(msg):
    doc = nlp(msg)
    entities = list(ent.text for ent in doc.ents)
    for e in entities:
        if e in diseases:
            selected_disease = e
            return e
        else:
            return selected_disease


def response(msg): # use this function to retrieve response for the user_input
    retrieved_res = "Sorry! I don't understand" # default if all else fails

    msg_words = nltk.word_tokenize(msg)
    msg_words = [lemmatizer.lemmatize(w) for w in msg_words]
    bag = []
    for word in words:
        if word in msg_words:
            bag.append(1)
        else:
            bag.append(0)

    selected_disease = predict_disease(msg)

    # Using the model
    # To find the class with highest probability, sorting is done
    prediction = model.predict(np.array([bag]))             
    # >>> prediction = [a1 a2 a3 a4 a5 a6....an]
    error_threshold = 0.25
    results = [[i, r] for i, r in enumerate(prediction) if r > error_threshold]
    # >>> results = [[0, p0], [1, p1], ... [n, p(n-1)]]
    
    results.sort(key=lambda x: x[1], reverse = True)
    # "key=lambda x: x[1]" is a lambda function
    # key -> [lambda[for all tuples 'x' select it's second element]]
    # reverse the order => descending order

    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        # Hash table or dictionary with key: value pairs "intent": "tag"
    intent_tag = return_list[0]["intent"]
    # [0] means the first element in the list and 
    # ["intent"] gives the value associated with the key "intent"
    # returns intent with highest probability
    for each_disease in responses["responses"]:
        if each_disease["tag"] == selected_disease:
            retrieved_res = random.choice(list(each_disease[intent_tag]))
            break
        else:
            retrieved_res = random.choice(list(each_disease["limit_reached"]))
    return retrieved_res

print("User: treatment of tuberculosis")
print("Bot: ", response("treatment of tuberculosis"))