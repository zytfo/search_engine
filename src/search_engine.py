# -*- coding: utf-8 -*-

import json
import src.document_parser as dp
import nltk

# terms = dp.parse()
dump = open('/Users/Artur/Desktop/University/Information Retrieval/Search Engine/src/dump', 'r')  # w+ to write
# dump.write(json.dumps(terms))
terms = json.loads(dump.read())

def intersect(p1, p2, disj):
    answer = []
    p1_index = 0
    p2_index = 0
    while p1_index != len(p1) and p2_index != len(p2):
        if p1[p1_index] == p2[p2_index]:
            answer.append(p1[p1_index])
            p1_index += 1
            p2_index += 1
        elif p1[p1_index] < p2[p2_index]:
            if disj == True:
                answer.append(p1[p1_index])
            p1_index += 1
        else:
            if disj == True:
                answer.append(p2[p2_index])
            p2_index += 1
    return answer

def get_rest(lst):
    rest_list = []
    for i in range(1, len(lst)):        
        rest_list.append(lst[i])
    return rest_list

def read_input(text):
    #print("Write you sentence")
    words = nltk.word_tokenize(text)
    fixed = []
    for word in words:
        word = dp.fix_token(word)
        fixed.append(word)
    return fixed

def multi_intersect(words):
    lst = []
    trms = []
    result = []
    non_exist = ''
    cont = True
    for word in words:
        if word not in terms:
            non_exist += str(word) + ' '
            cont = False
        else:
            lst.append(terms.get(word))
    if cont == False:
        return ("There is no word(s) " + non_exist + " in documents. Try another query.")
    else:
        lst = sorted(lst, key = len)
        result = lst[0]                  # first in asc
        trms = get_rest(lst)
        while len(trms) != 0 and len(result) != 0:
            result = intersect(result, trms[0], False)
            trms = get_rest(trms)
        return result

def main(text):
    return multi_intersect(read_input(text))