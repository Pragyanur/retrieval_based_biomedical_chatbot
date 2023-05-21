import random
import json
import pickle
import nltk
import spacy
import numpy as np
from nltk.stem import WordNetLemmatizer
import keras
from keras.models import load_model

nlp = spacy.load("en_core_sci_sm")
model = load_model("intent_classification.h5", compile=False)

words = pickle.load(open("pickles/words.pkl", "rb"))
diseases = pickle.load(open("pickles/diseases.pkl", "rb"))
classes = pickle.load(open("pickles/classes.pkl", "rb"))

def predict_disease(msg):
    doc = nlp(msg)
    entities = list(ent.text for ent in doc.ents)
    for e in entities:
        if e in diseases:
            return e
        else:
            return "none"
