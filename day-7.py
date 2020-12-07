import re


def file_reader(file):
    with open(file, 'r') as f:
        for row in f:
            yield row.strip()


# --- Solution one ---

def count_parent_bags():
    res = 0
    bags = []

    def find_parents(bag):
        nonlocal res
        for line in file_reader("bags.txt"):
            parent, children = line.split(' bags contain')
            if bag in children and parent not in bags:
                bags.append(parent)
                res += 1
                find_parents(parent)

    find_parents('shiny gold')
    return res


# --- Solution two ---

def count_child_bags():
    res = 0

    def find_children(bag, parent_number):
        nonlocal res
        for line in file_reader("bags.txt"):
            parent, children = line.split(' bags contain')
            if bag in parent:
                child_list = children.strip()[:-1].split(', ')
                for child in child_list:
                    match = re.search(r"(\d) ([a-z ]+) (bag)", child)
                    if match:
                        number = match.group(1)
                        color = match.group(2)
                        res += int(number) * parent_number
                        find_children(color, int(number) * parent_number)

    find_children('shiny gold', 1)
    return res
