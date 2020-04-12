import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

import re
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd 
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier  
import numpy as np


nlp = en_core_web_sm.load()

class OrderEmailRecognition:
	def __init__(self):
		self.vectorizer = pickle.load(open("tfidf.pkl", "rb"))
		self.model = pickle.load(open("svm_model.pkl", "rb"))
	
	def isDocOrderNotification(self, raw_doc):
		x_input = self.buildTFIDF(raw_doc)
		return self.model.predict(x_input)[0]

	def buildTFIDF(self, raw_doc):
		doc = remove_entity_words(raw_text)
		corpus = [doc]
		return self.vectorizer.transform(corpus)

	def extractEntities(self, raw_doc):
		return nlp(raw_doc).ents

def clean_raw_text(raw_text):
    soup = BeautifulSoup(raw_text, 'html.parser')
    clean_soup = repr(soup.get_text().replace('\n','.'))
    clean_soup = re.sub(r'\\x[0-9A-Fa-f]{2}', ' ', clean_soup)
    clean_soup = re.sub(r'\\u[0-9A-Fa-f]{4}', ' ', clean_soup)
    clean_soup = re.sub(r'[\.] +', '.', clean_soup)
    clean_soup = re.sub(r'\.+', '. ', clean_soup)
    clean_soup = re.sub(' +', ' ', clean_soup)
    return clean_soup

def remove_entity_words(raw_text):
    input_text = clean_raw_text(raw_text)
    tags = nlp(input_text)
    for entity in tags.ents:
        tag = entity.label_
        text = entity.text
#         print(tag, text)
        if tag in ['PERSON', 'ORG', 'EVENT', 'GPE', 'NORP', 'PRODUCT', 'MONEY']:
            input_text = input_text.replace(text, tag)
    return input_text


