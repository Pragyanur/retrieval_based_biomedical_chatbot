import random
import json
import pickle
import nltk
import spacy
import numpy as np
from nltk.stem import WordNetLemmatizer
import keras
from keras.models import load_model
from training_model import words, ignore_words, classes, diseases

nlp = spacy.load("en_core_sci_sm")
model = load_model("intent_classification.h5", compile = False)

text = """Myeloid derived suppressor cells (MDSC) are immature 
myeloid cells with immunosuppressive activity. Lung cancer
They accumulate in tumor-bearing mice and humans 
with different types of cancer, including hepatocellular 
carcinoma (HCC)."""

doc = nlp(text)

entities = list(ent.text for ent in doc.ents)

print(entities)

def check_disease(msg):
    doc = nlp(msg)
    entities = list(ent.text for ent in doc.ents)
    for e in entities:
        if e in diseases:
            return e

# if e not in list_of_diseases
# response tag "none"

print(check_disease("tuberculosis"))