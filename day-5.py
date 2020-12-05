from math import floor, ceil


def file_reader(file):
    for row in open(file, 'r'):
        yield row


def binary_partitioning(binary, index, lower, upper):
    difference = (upper - lower) / 2
    if difference < 1:
        if binary[0] in 'FL':
            return lower
        else:
            return upper
    if binary[0] in 'FL':
        return binary_partitioning(binary[1:], lower, floor(lower + difference))
    else:
        return binary_partitioning(binary[1:], ceil(lower + difference), upper)


ids = [8 * binary_partitioning(seat, 0, 127) + binary_partitioning(seat, 0, 7) for seat in file_reader("plane.txt")]

# First solution
print(max(ids))

# Second solution
prev = float('-inf')
for curr in sorted(ids):
    if curr - prev == 2:
        print(prev + 1)
    prev = curr
