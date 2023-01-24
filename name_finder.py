import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

from bs4 import BeautifulSoup
import requests
import re

import json

def loadjson():
    #Load in JSON
    #JSON Structure:
    # { "text": whatever the text of the tweet holds
    #   "user": {screen name, user id}
    #   "id": tweet id
    #   "timestamp_ms": time of tweet (Long float structure)
    # }

    file = open("Data/gg2013.json")
    data = json.load(file)
    test_data = ""
    return data


tweetdata = loadjson()
full_string = ""
for object in tweetdata[:200]:
    full_string += object["text"]


doc = nlp(full_string)
len(doc.ents)
labels = [x.label_ for x in doc.ents]     #tells us the number of words in each category
#print(Counter(labels))

names = [x.text for x in doc.ents if x.label_ == "PERSON"]
print(names)



items = [x.text for x in doc.ents]
#print(Counter(items).most_common(3))      #tells us the three most common terms

sentences = [x for x in doc.sents]
#print(sentences[20])