def load_homework():
    with open('inputs/homework.txt', 'r') as file:
        return file.readlines()


def evaluate_expression(expression: list):
    stack = []
    for i, x in enumerate(expression):
        if x == '(':
            stack.append(i)
        elif x == ')':
            start = stack.pop()
            expression[start: i + 1] = evaluate_brackets(expression[start + 1: i])
            return evaluate_expression(expression)
    return evaluate_brackets(expression)


def perform_operation(pre, operation, post):
    if operation == '+':
        return float(pre) + float(post)
    elif operation == '*':
        return float(pre) * float(post)


def evaluate_brackets(expression: list):
    while '+' in expression:  # Added for solution 2 - Remove for solution 1
        i = expression.index('+')
        pre, operation, post = expression[i-1: i+2]
        expression = expression[:i-1] + [perform_operation(pre, operation, post)] + expression[i+2:]
    while len(expression) > 1:
        pre, operation, post = expression[0: 3]
        expression = [perform_operation(pre, operation, post)] + expression[3:]
    return expression


res = 0
for task in load_homework():
    res += evaluate_expression(task.strip().split(' '))[0]
print(res)
