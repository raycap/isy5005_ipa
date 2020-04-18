import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import nltk
import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd 
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import json

nlp = en_core_web_sm.load()

class OrderEmailRecognition:
    def __init__(self):
        self.vectorizer = pickle.load(open("model/tfidf.pkl", "rb"))
        self.model = pickle.load(open("model/svm_model.pkl", "rb"))
        with open('model/order_status_sample.json') as json_file:
            self.order_status_sample_list = json.load(json_file)
#        print(self.order_status_sample_list)
    def isDocOrderNotification(self, raw_doc):
        x_input = self.buildTFIDF(raw_doc)
        return self.model.predict(x_input)[0]

    def buildTFIDF(self, raw_doc):
        doc = remove_entity_words(raw_doc)
        corpus = [doc]
        return self.vectorizer.transform(corpus)

    def extractEntities(self, raw_doc):
        return nlp(raw_doc).ents
    
    def extractOrderStatusRelatedText(self, raw_doc):
        if raw_doc == '' or raw_doc == None:
            return ''
        doc = clean_raw_text(raw_doc)
        raw_texts_0 = nltk.sent_tokenize(doc)
        raw_texts = []
        # Remove anything less than 3 words
        for raw_text in raw_texts_0:
            if len(raw_text.split(' ')) < 3:
                continue
            raw_texts.append(raw_text)
        # Masked specific details, i.e. email, person name
        masked_raw_texts = []
        for raw_text in (raw_texts):
            masked_raw_texts.append(remove_entity_words(raw_text))
        sim_metrics = np.zeros((len(masked_raw_texts),len(self.order_status_sample_list)))
        for i in range(len(masked_raw_texts)):
            for j in range(len(self.order_status_sample_list)):
                text = masked_raw_texts[i]
                sentence = self.order_status_sample_list[j]
                sim_metrics[i,j] = get_cosine_sim(text, sentence)[0,1]
        return raw_texts[np.argmax(np.amax(sim_metrics, axis=1))]

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
    input_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '_url_page_', input_text)
    input_text = re.sub(r'[\w\.-]+@[\w\.-]+', '_email_replaced_', input_text)
    tags = nlp(input_text)
    for entity in tags.ents:
        tag = entity.label_
        text = entity.text
        if tag in ['PERSON', 'ORG', 'EVENT', 'GPE', 'NORP', 'PRODUCT', 'MONEY']:
            input_text = input_text.replace(text, '_'+tag+'_')
    return input_text

def get_cosine_sim(*strs): 
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)
    
def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()