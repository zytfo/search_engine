# -*- coding: utf-8 -*-

import json
import document_parser as dp
import nltk
import collections
import os

#terms = dp.parse()
counter = 1
dir = os.path.dirname(__file__)
relative_path = os.path.join(dir, './dump')
dump = open(relative_path, 'r')  # w+ to write
#dump.write(json.dumps(terms))
terms = json.loads(dump.read())

def intersect(p1, p2, operation):
    answer = []
    p1_index = 0
    p2_index = 0
    while p1_index != len(p1) and p2_index != len(p2):
        if p1[p1_index] == p2[p2_index]:
            answer.append(p1[p1_index])
            p1_index += 1
            p2_index += 1
        elif p1[p1_index] < p2[p2_index]:
            if operation == 'OR':
                answer.append(p1[p1_index])
                p1_index += 1
            elif operation == 'AND':
                p1_index += 1
        else:
            if operation == 'OR':
                answer.append(p2[p2_index])
                p2_index += 1
            elif operation == 'AND':
                p2_index += 1
    return answer

def shunting_yard(input):
    order = {'(': 0, ')': 0, 'OR': 1, 'AND': 2, 'NOT': 3}
    output = []
    stack = []
    for token in input:
        if token == '(':
            stack.append(token)
        elif token == ')':
            operator = stack.pop()
            while operator != '(':
                output.append(operator)
                operator = stack.pop()
        elif token in order:
            if stack:
                current_op = stack[-1]
                while stack and order[current_op] > order[token]:
                    output.append(stack.pop())
                    if stack:
                        current_op = stack[-1]
            stack.append(token)
        else:
            output.append(token.lower())
    while stack:
        output.append(stack.pop())
    return output

def negation(term_indexes):
    result = []
    terms_index = list(range(1, len(terms)))
    if not term_indexes:
        return term_indexes
    i = 0
    for item in terms_index:
        if item != term_indexes[i]:
            result.append(item)
        elif i + 1 < len(term_indexes):
            i += 1
    return result

def parse(query):
    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query = query.split(' ')
    cont = True
    stack = []
    st = ''
    non_exist = ''
    stemmer = nltk.stem.porter.PorterStemmer()
    for i in range(0, len(query)):
        st += dp.fix_token(query[i]) + " "
    queue = collections.deque(shunting_yard(st.split()))
    for word in queue:
        word = stemmer.stem(word)
        if word not in ['AND', 'OR', 'NOT'] and word not in terms:
            non_exist += str(word) + ' '
            cont = False
    if cont == False:
        return ("There is no word(s) " + non_exist + "in documents. Try another query.")
    queue = collections.deque(shunting_yard(query))

    while queue:
        token = queue.popleft()
        result = []
        if token != 'AND' and token != 'OR' and token != 'NOT':
            token = stemmer.stem(token)
            if token in terms:
                result = terms[token]
        elif token == 'AND':
            result = intersect(stack.pop(), stack.pop(), 'AND')
        elif token == 'OR':
            result = intersect(stack.pop(), stack.pop(), 'OR')
        elif token == 'NOT':
            result = negation(stack.pop())
        stack.append(result)
    if len(stack) != 1:
        return "Something went wrong. Don't forget to write either AND, OR or NOT in multiple query. You can use scopes as well"
    return stack.pop()

'''
Works withound boolean expression handler for queries like: information retrieval
'''
def get_rest(lst):
    rest_list = []
    for i in range(1, len(lst)):
        rest_list.append(lst[i])
    return rest_list

def multi_intersect(words, operation):
    lst = []
    trms = []
    result = []
    default_operation = 'AND'
    non_exist = ''
    cont = True
    if len(words) == 1 and operation == '':
        None
    elif operation not in ['AND', 'OR', 'NOT']:
        return "An operation should be either AND, OR or NOT."
    for word in words:
        if word not in terms:
            non_exist += str(word) + ' '
            cont = False
        else:
            lst.append(terms.get(word))
    if cont == False:
        return "There is no word(s) " + non_exist + " in documents. Try another query."
    else:
        lst = sorted(lst, key = len)
        result = lst[0]                  # first in desc
        trms = get_rest(lst)
        while len(trms) != 0 and len(result) != 0:
            result = intersect(result, trms[0], operation)
            trms = get_rest(trms)
        return result

def main(query):
    return parse(query)