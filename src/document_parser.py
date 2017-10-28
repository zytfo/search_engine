# -*- coding: utf-8 -*-
'''
    Parse bunch of documents into tokens
'''
import nltk
import re
import os
import json

'''
    Splitting LISA arhchives into the bunch of documents
'''
def split():
    counter = 1
    dir = os.path.dirname(__file__)
    for i in range(1, 15):
        relative_path = os.path.join(dir, '../Archives/' + str(i) + '.txt')
        with open(relative_path) as file:
            for line in file:
                path = os.path.join(dir, '../Documents/' + str(counter) + '.txt')
                file = open(path, 'a')
                if line.find("********************************************") == -1:
                    if 'Document' not in line:
                        file.write(line)
                else:
                    file.close()
                    counter += 1

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def parse():
    terms = {}
    stemmer = nltk.stem.porter.PorterStemmer()
    dir = os.path.dirname(__file__)
    for docID in range(1, 6005):
        relative_path = os.path.join(dir, '../Documents/' + str(docID) + '.txt')
        with open(relative_path) as file:
            tokens = nltk.word_tokenize(file.read())
            for j in range(0, len(tokens)):
                tokens[j] = stemmer.stem(fix_token(tokens[j].lower()))
            tokens = remove_values_from_list(tokens, '')
            for word in tokens:
                if word not in terms:
                    terms.update({word:{docID:1}})
                else:
                    if docID in terms[word]:
                        terms[word][docID] += 1
                    else:
                        terms[word][docID] = 1
    return terms

def fix_token(token):
    token = re.sub(r'[^\w\s]','', token)
    return token
