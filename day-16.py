import re

with open('inputs/tickets.txt', 'r') as file:
    raw_rules, my_ticket, raw_tickets = file.read().split('\n\n')

# --- Reformatting the rules ---

raw_rules = raw_rules.split('\n')
re_rule = re.compile(r'\D+:')
re_ranges = re.compile(r'\d+-\d+')


def format_rules():
    res = {}
    for rule in raw_rules:
        key = re.search(re_rule, rule).group()[:-1]
        values = re.findall(re_ranges, rule)
        res.update({key: []})
        for value in values:
            lower, upper = value.split('-')
            res[key].append((int(lower), int(upper)))
    return res


rules = format_rules()  # Format ---> {'field' : [(lower_1, upper_1), (lower_2, upper_2)], ... }


# --- Reformatting the tickets ---

def reformat_tickets():
    res = []
    for ticket in raw_tickets.split('\n')[1:]:
        res.append(list(map(int, ticket.split(','))))
    return res


tickets = reformat_tickets()  # Format ---> [[34, 21, 77, ...], ...]

# --- Reformatting my ticket ---

my_ticket = list(map(int, my_ticket.split(',')[1:]))  # Format ---> [45, 43, 102, ...]


# --- Solution 1 ---

def invalid_fields(number: int):
    for field in rules.values():
        for lower, upper in field:
            if lower <= number <= upper:
                return 0  # Field is valid
    return number  # Field is invalid


def sum_invalid_fields(ticket: list):
    return sum(map(invalid_fields, ticket))


# print(sum(map(sum_invalid_fields, tickets)))


# --- Solution 2 ---

def is_field_valid(number: int):
    for field in rules.values():
        for lower, upper in field:
            if lower <= number <= upper:
                return True
    return False


def ticket_is_valid(ticket: list):
    return all(map(is_field_valid, ticket))


valid_tickets = [ticket for ticket in tickets if ticket_is_valid(ticket)]


def transpose_matrix(matrix):
    transpose = []
    for i in range(len(matrix[0])):
        row = []
        for j in range(len(matrix)):
            row.append(matrix[j][i])
        transpose.append(row)
    return transpose


def check_match(number: int, field_ranges: list):
    for lower, upper in field_ranges:
        if lower <= number <= upper:
            return True
    return False


def determine_fields():
    """
    :return: Dictionary in the format {0: 'field', ...} where the keys correspond to the index of the elements on the
    tickets and the values correspond to the field
    """
    possible = {}
    fields = list(rules.keys())
    while len(fields) > 0:
        field_name = fields.pop()
        field_ranges = rules[field_name]
        possible.update({field_name: []})
        for i, field in enumerate(transpose_matrix(valid_tickets)):
            if all(map(lambda num: check_match(num, field_ranges), field)):
                possible[field_name].append(i)
    res = {}
    for key, values in dict(sorted(possible.items(), key=lambda item: len(item[1]))).items():
        for value in values:
            if value not in res:
                res.update({value: key})
                break
    return res


ans = 1
for index, category in determine_fields().items():
    if 'departure' in category:
        ans *= my_ticket[index]

print(ans)
