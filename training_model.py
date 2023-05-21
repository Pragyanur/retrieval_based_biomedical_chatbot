import random
import json
import pickle
import nltk
import spacy
from nltk.stem import WordNetLemmatizer
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

nlp = spacy.load("en_core_sci_sm")

text = """Myeloid derived suppressor cells (MDSC) are immature 
myeloid cells with immunosuppressive activity. Lung cancer
They accumulate in tumor-bearing mice and humans 
with different types of cancer, including hepatocellular 
carcinoma (HCC)."""
di = """tuberculosis lung cancer"""

doc = nlp(text)
list_of_disease = nlp(di)

entities = list(ent.text for ent in doc.ents)
disease_list = list(ent.text for ent in list_of_disease.ents)

print(entities)
print(disease_list)

def check_disease(msg):
    doc = nlp(msg)
    entities = list(ent.text for ent in doc.ents)
    for e in entities:
        if e in list_of_disease:
            return e

# if e not in list_of_diseases
# response tag "none"

lemmatizer = WordNetLemmatizer()

words = []                  # set of words in the dataset intents.json
diseases = []               # diseases in responses.json
documents = []              # list(words in pattern, corresponding tag)
classes = []                # intent classes from intents.json
ignore_words = ["?", "!", ".", ","]

file = open("responses.json", "r", encoding = "UTF-8")
data = json.load(file)

for disease in data["responses"]:
    d = data["disease"]
    diseases.extend(d)

print(diseases)

file = open("intents.json", "r", encoding = "UTF-8")
intents = json.load(file)

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        w =  nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent["tag"]))

    if intent["tag"] not in classes:
        classes.append(intent["tag"])

# pre-process and organise the data
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
diseases = sorted(list(set(diseases)))


print(len(documents), " documents")
print("Documents: ", documents)
print(len(words), "unique lemmatized words", words)
print("diseases: ", diseases)
print("classes: ", classes)
print("")

pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(diseases, open("diseases.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

training = []
output_empty = [0] * len(classes) # symptoms, cure

for doc in documents:
    bag = []
    pattern_words = doc[0]
    for w in words:
        if w in pattern_words:
            bag.append(1)
        else:
            bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
train_x = np.array([i[0] for i in training])
train_y = np.array([i[1] for i in training])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

sgd=SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

HIST = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save("intent_classification.h5", HIST)