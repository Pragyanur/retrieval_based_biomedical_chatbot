import json
import pickle
from chatbot import predict_disease
from utility import check_intent, check_disease

# loading the files
txt_responses = open("responses.txt", "r", encoding="UTF-8").read()
sections = txt_responses.split("\n\n")


with open("response.json", "r") as file:
    responses = json.load(file)


diseases = pickle.load(open("pickles/diseases.pkl", "rb"))
intents = pickle.load(open("pickles/classes.pkl", "rb"))

# for s in sections:
#     dis = check_disease(s)
#     tag = check_intent(s)
# print("disease: ", dis, ", intent: ", tag)
# for t in responses["responses"]:
#     if t["tag"] == d:
#         t[tag] = s
#         break

with open("responses.json", "w") as x:
    json.dump(responses, x, indent=3)

count = 25
for item in responses["responses"]:
    if item["tag"] == "malaria":
        for w in intents:
            if w == "none":
                continue
            item[w] = sections[count]
            count += 1


with open("responses.json", "w") as x:
    json.dump(responses, x, indent=3)
file.close()
x.close()
