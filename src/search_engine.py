# -*- coding: utf-8 -*-

import json
import document_parser as dp
import nltk
import collections
import os
import math
import operator

counter = 1
dir = os.path.dirname(__file__)
relative_path = os.path.join(dir, './dump')
dump = open(relative_path, 'r')  # w+ to write
terms = json.loads(dump.read())
final_scores = {}
N = 6004

def parse(query):
    query_tokens = {}
    tokens = nltk.word_tokenize(query)
    stemmer = nltk.stem.porter.PorterStemmer()
    for i in range(0, len(tokens)):
        tokens[i] = stemmer.stem(dp.fix_token(tokens[i].lower()))
    tokens = dp.remove_values_from_list(tokens, '')
    for token in tokens:
        if token not in query_tokens:
            query_tokens.update({token:1})
        else:
            query_tokens[token] += 1
    return calculateScores(query_tokens)


def calculateScores(query_tokens):
    temp_scores = {}
    scores_for_query = queryScores(query_tokens)
    scores_for_document = documentScores(query_tokens)
    for term in scores_for_query:
        docs = scores_for_document.get(term)
        if docs == None:
            continue
        else:
            for docID in docs:
                if term not in temp_scores:
                    temp_scores.update({term: {docID: scores_for_query.get(term) * scores_for_document[term].get(docID)}})
                else:
                    for docID in docs:
                        temp_scores[term][docID] = scores_for_query.get(term) * scores_for_document[term].get(docID)
    for term in temp_scores:
        for docID in temp_scores[term]:
            if docID not in final_scores:
                final_scores.update({docID:temp_scores[term][docID]})
            else:
                final_scores[docID] += temp_scores[term][docID]
    return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)


def documentScores(tokens):
    document_scores = {}
    document_length = 0
    for token in tokens:
        document_scores.update({token:terms.get(token)})
    for term in document_scores:
        if document_scores.get(term) != None:
            for docID in document_scores[term]:
                document_scores[term][docID] = 1 + math.log10(document_scores[term][docID])
                document_length += document_scores[term][docID]**2
    document_length = math.sqrt(document_length)
    for term in document_scores:
        if document_scores.get(term) != None:
            for docID in document_scores[term]:
                document_scores[term][docID] = document_scores[term][docID] / document_length
    return document_scores

def queryScores(tokens):
    query_scores = {}
    query_length = 0
    for token in tokens:
        tf = 1 + math.log10(tokens[token])
        terms_from_token = terms.get(token)
        if terms_from_token != None:
            idf = math.log10(N / len(terms_from_token))
        else:
            idf = None
        if tf != None and idf != None:
            tf_idf = tf * idf
            query_scores.update({token:tf_idf})
            query_length += tf_idf**2
    query_length = math.sqrt(query_length)
    for token in query_scores:
        query_scores[token] = query_scores[token] / query_length
    return query_scores

def main(query):
    return parse(query)

