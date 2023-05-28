import random
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD


lemmatizer = WordNetLemmatizer()

words = []  # set of words in the dataset intents.json
diseases = []  # diseases in responses.json
documents = []  # list(words in pattern, corresponding tag)
classes = []  # intent classes from intents.json
ignore_words = ["?", "!", "XXXX", ".", ",", "disease"]

file = open("responses.json", "r", encoding="UTF-8")
data = json.load(file)

for disease in data["responses"]:
    d = disease["tag"]
    diseases.append(d)


file = open("intents.json", "r", encoding="UTF-8")
intents = json.load(file)

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        w = nltk.word_tokenize(pattern)
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

# print("Documents: ", documents)
print(len(words), "unique lemmatized words", words)
print("diseases: ", diseases)
print("classes: ", classes)
print("")

pickle.dump(words, open("pickles/words.pkl", "wb"))
pickle.dump(diseases, open("pickles/diseases.pkl", "wb"))
pickle.dump(classes, open("pickles/classes.pkl", "wb"))

training = []
output_empty = [0] * len(classes)

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
model.add(Dense(144, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

HIST = model.fit(
    np.array(train_x), np.array(train_y), epochs=1000, batch_size=5, verbose=1
)
model.save("intent_classification.h5", HIST)

print("model trained and saved")
