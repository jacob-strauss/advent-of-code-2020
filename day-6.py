# --- Solution 1 ---
print(sum([len(set(group)) for group in [x.replace('\n', '') for x in open("declaration.txt", 'r').read().split('\n\n')]]))

# --- Solution 2 ---

from collections import Counter

res = 0
for group in [x.split('\n') for x in open("declaration.txt", 'r').read().split('\n\n')]:
    shared = Counter()
    for y in group:
        for z in y:
            shared[z] += 1
            if shared[z] == len(group):
                res += 1
print(res)
