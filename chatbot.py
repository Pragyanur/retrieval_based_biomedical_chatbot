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

responses_starts = open("responses.json", "r", encoding="UTF-8")
responses = json.load(responses_starts)

words = pickle.load(open("pickles/words.pkl", "rb"))
diseases = pickle.load(open("pickles/diseases.pkl", "rb"))
classes = pickle.load(open("pickles/classes.pkl", "rb"))
# ignore_words = pickle.load(open("pickles/ignore_words.pkl", "rb"))
ignore_words = ["?", "!", "XXXX"]


def predict_disease(msg, prev_disease):
    doc = nlp(msg)
    entities = list(ent.text for ent in doc.ents)
    for e in entities:
        if e in diseases:
            prev_disease = e
            return e
        else:
            continue
    return prev_disease


def response(msg, dis):  # use this function to retrieve response for the user_input
    retrieved_res = "Sorry! I don't understand"  # default if all else fails
    predicted_disease = predict_disease(msg, dis)

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

    print("[looking for: ", intent_tag, " | disease: ", predicted_disease, "]")
    # if "tag" matches the predicted disease then choose any of the random responses
    for item in all_disease:
        if item["tag"] == predicted_disease:
            retrieved_res = random.choice(item[intent_tag])
            return retrieved_res
