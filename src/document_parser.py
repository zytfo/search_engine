# -*- coding: utf-8 -*-
'''
    Parse bunch of documents into tokens
'''
import nltk
import re

def parse():
    terms = {}
    stemmer = nltk.stem.porter.PorterStemmer()
    for i in range(1, 6005):
        with open('/Users/Artur/Desktop/University/Information Retrieval/Search Engine/Documents/' + str(i) + '.txt') as file:
            tokens = nltk.word_tokenize(file.read())
            for word in tokens:
                word = stemmer.stem(fix_token(word.lower()))
                if word not in terms:
                    if word != '':
                        terms.update({word:[i]})
                elif i not in terms.get(word):
                    terms[word].append(i)
    return terms

def fix_token(token):
    token = re.sub(r'[^\w\s]','', token)
    return token