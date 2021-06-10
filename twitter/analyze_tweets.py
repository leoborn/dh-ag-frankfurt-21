"""
This script is used to analyze the 100 tweets we obtained in get_tweets.py (in tweets.obj).

The exercise part of this script is not included.

Run this script like this: python analyze_tweets.py
"""

# Since we saved our tweets of interest in a binary file, we need pickle to read them again.
import pickle
# Since we want to report some statistics, we import FreqDist.
from nltk import FreqDist
import spacy
# We initialize a Japanese NLP pipeline with the medium-sized language model.
nlp = spacy.load('ja_core_news_md')

with open("./tweets.obj", "rb") as my_file:
    original_tweets = pickle.load(my_file)

# Task: Get all named entities in the tweets by type
named_entities_by_type = {}
for tweet in original_tweets:
    if tweet.lang == "ja":
        print("Tweet:", tweet.full_text)
        doc = nlp(tweet.full_text)
        for named_entity in doc.ents:
            ne = named_entity.text
            ne_label = named_entity.label_
            print(ne, ne_label)
            # Why is this step necessary?
            if ne_label not in named_entities_by_type:
                named_entities_by_type[ne_label] = []
            named_entities_by_type[ne_label].append(ne)

print(named_entities_by_type)

products = named_entities_by_type["PRODUCT"]
fdist = FreqDist(products)
print(fdist.most_common(20))

# Sub-task: Is the glass full or half full?
# What was the problem above?
import unicodedata
normalized_products = []
for prod in products:
    norm_prod = unicodedata.normalize('NFKC', prod)
    normalized_products.append(norm_prod)

fdist = FreqDist(normalized_products)
print(fdist.most_common(20))