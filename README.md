# RETRIEVAL BASED BIOMEDICAL CHATBOT

Retrieval based biomedical chatbot to answer know bouts of various diseases

## Technologies used
- Keras three layers sequential model to classify the type of fact
- spaCy biomedical text processing models for disease classification
- NLTK for tokenization, lemmatization, and lowercasing words
- pickle files to store lists of data
- "intent_classification.h5" to save the trained model

## Process
- From patterns create bag of words after pre-processing
- Words from the patterns along with their corresponding tag/classes are stored as document list of tupples
- List of unique words, classes and disease are stored as pickle files in a separate folder
- A list for training (train_x and train_y) is produced from documents list:
  - train_x is a binary list representing the presence of unique words in each pattern
  - train_y is a binary list that has '1' only for the class/tag that match the pattern
- Keras sequential (128 relu, 64 relu, output_row softmax) with SGD as the optimizer is created
- Model is compiled with 'categorical cross entropy' as the loss function, 1000 epochs in batch of 5 and saved
