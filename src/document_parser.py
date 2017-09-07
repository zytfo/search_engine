# -*- coding: utf-8 -*-
'''
    Parse bunch of documents into tokens
'''
import nltk
import re

'''
    Splitting LISA arhchives into the bunch of documents
'''
def split():
    counter = 1
    for i in range(1, 15):
        with open('/Users/Artur/Desktop/lisa/Archives/LISA' + str(i)) as file:
            for line in file:
                file = open('/Users/Artur/Desktop/lisa/Documents/' + str(counter) + '.txt', 'a')
                if line.find("********************************************") == -1:
                    if 'Document' not in line:
                        file.write(line)
                else:
                    file.close()
                    counter += 1

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