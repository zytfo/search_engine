import nltk

def shunting_yard(input):
    order = {}
    order['('] = 0
    order[')'] = 0
    order['OR'] = 1
    order['AND'] = 2
    order['NOT'] = 3

    output = []
    stack = []
    oeprator = ''
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