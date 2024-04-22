import pickle
import spacy
import nltk
import json
from nltk import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
ignore_words = ["?", "!", "XXXX", "disease"]

def view_diseases():
    li = pickle.load(open("data/diseases.pkl", "rb"))
    diseases = list(i for i in li if i != "none")
    return diseases

def view_intents():
    li = pickle.load(open("data/classes.pkl", "rb"))
    print(li)

def check_intent(msg):
    msg_words = nltk.word_tokenize(msg)
    msg_words = [
        lemmatizer.lemmatize(w.lower()) for w in msg_words if w not in ignore_words
    ]
    ints = pickle.load(open("data/classes.pkl", "rb"))
    for w in msg_words:
        if w in ints:
            return w
    return "none"

def check_disease(msg):
    msg_words = nltk.word_tokenize(msg)
    msg_words = [
        lemmatizer.lemmatize(w.lower()) for w in msg_words if w not in ignore_words
    ]
    dis = pickle.load(open("data/diseases.pkl", "rb"))
    for w in msg_words:
        if w in dis:
            return w
    return "none"

def textPP(text): # returns a list of tokenized, lemmatized, lower cased words from text and removes ignore_words
    words = nltk.word_tokenize(text)
    words = [
        lemmatizer.lemmatize(w.lower()) for w in text if w not in ignore_words
    ]
    return words

def predict_spacy(text):
    nlp = spacy.load("en_ner_bc5cdr_md")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(entities)

# training 2

def openJSON(url):
    file = open(url, "r", encoding="utf-8")
    data = json.load(file)
    return data

def readPickle(url):
    file = open(url, "rb")
    data = pickle.load(file)
    return data

def writePickle(url, data):
    file = open(url, "wb")
    pickle.dump(data, file)
    print(data, "\n\nwritten to ", url)
