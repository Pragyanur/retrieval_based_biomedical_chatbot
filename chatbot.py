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


def response(msg):
    msg_words = nltk.word_tokenize(msg)
    msg_words = [lemmatizer.lemmatize(w) for w in msg_words]
    bag = []
    for word in words:
        if word in msg_words:
            bag.append(1)
        else:
            bag.append(0)

    disease = predict_disease(msg)
    prediction = model.predict(np.array([bag]))
    error_threshold = 0.25
    results = [[i, r] for i, r in enumerate(prediction) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]]})

