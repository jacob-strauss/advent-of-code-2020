import re


def initialisation_program():
    with open('inputs/initialization program.txt', 'r') as file:
        for line in file:
            yield line.strip().split(' = ')


def integer_converter(num):
    return '{0:036b}'.format(num)


def binary_converter(num):
    return int(num, 2)


# --- Solution 1 ---

def apply_mask(mask, num):
    res = ''
    for i in range(36):
        if mask[i] == 'X':
            res += num[i]
        else:
            res += mask[i]
    return res


def chip_decoder_v1():
    memory = {}
    mask = ''
    for instruction, value in initialisation_program():
        if instruction == 'mask':
            mask = value
        else:
            binary = integer_converter(int(value))
            altered_binary = apply_mask(mask, binary)
            address = re.search(r'\d+', instruction).group()
            memory.update({address: altered_binary})
    return sum(map(binary_converter, memory.values()))


# --- Solution 2 ---

def memory_address_decoder(mask: str, memory: str):
    """
    Applies a mask to a memory address. If value is 'X' creates two new 'branches' and adds them to the list of all
    possible memory address.

    :param mask: 36-bit binary string.
    :param memory: 36-bit binary string.
    :return: The set of all possible memory addresses.
    """
    bucket = ['']
    for i in range(36):
        if mask[i] == '0':
            bucket = address_modifier(bucket, memory[i])
        elif mask[i] == '1':
            bucket = address_modifier(bucket, '1')
        else:
            bucket = address_modifier(bucket, '0') + address_modifier(bucket, '1')
    return bucket


def address_modifier(bucket: list, value: str):
    """
    Takes all values in a list, changes them accordingly, adds them to a new list, then returns the new list.

    :param bucket: A list of memory addresses expressed as 36-bit binary strings.
    :param value: The value to be add to each memory address.
    :return: The set of memory address each with the value added to it.
    """
    new_bucket = []
    bucket_copy = bucket[:]
    while len(bucket_copy) != 0:
        item = bucket_copy.pop()
        item += value
        new_bucket.append(item)
    return new_bucket


def chip_decoder_v2():
    memory = {}
    mask = ''
    for instruction, value in initialisation_program():
        if instruction == 'mask':
            mask = value
        else:
            address = re.search(r'\d+', instruction).group()
            binary_address = integer_converter(int(address))
            memory_set = memory_address_decoder(mask, binary_address)
            for location in memory_set:
                memory.update({location: int(value)})
    return sum(memory.values())
