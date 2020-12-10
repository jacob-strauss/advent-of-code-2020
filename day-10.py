with open('inputs/adaptors.txt', 'r') as file:
    adaptors = [int(x) for x in file.readlines()]

adaptors.insert(0, 0)
adaptors.sort()


# --- Solution 1 ---

def jolt_difference():
    adaptors.append(adaptors[-1] + 3)

    dist = {1: 0, 2: 0, 3: 0}
    for index in range(0, len(adaptors) - 1):
        dist[adaptors[index + 1] - adaptors[index]] += 1

    return dist[1] * dist[3]


# --- Solution 2 ---

branch_storage = {}


def branch(value):
    if value == adaptors[-1]:
        return 1
    if value in branch_storage:
        return branch_storage[value]
    permutations = 0
    for jump in range(1, 4):
        if value + jump in adaptors:
            permutations += branch(value + jump)
    return permutations


for adaptor in reversed(adaptors):
    branch_storage.update({adaptor: branch(adaptor)})

print(branch_storage[0])
