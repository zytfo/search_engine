# -*- coding: utf-8 -*-
'''
    Parse bunch of documents into tokens
'''
import nltk
import re
import os

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

def parse():
    terms = {}
    stemmer = nltk.stem.porter.PorterStemmer()
    dir = os.path.dirname(__file__)
    for i in range(1, 6005):
        relative_path = os.path.join(dir, '../Documents/' + str(i) + '.txt')
        with open(relative_path) as file:
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