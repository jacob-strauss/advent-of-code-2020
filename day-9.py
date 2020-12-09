with open("inputs/xmas.txt") as file:
    xmas = [int(line) for line in file.readlines()]


def check_valid(data: list, preamble: int):
    for x in range(preamble):
        for y in range(x + 1, preamble):
            if data[x] + data[y] == data[-1]:
                return True
    return False


def reconnaissance():
    for i in range(0, len(xmas) - 26):
        if not check_valid(xmas[i:i + 26], 26):
            return xmas[i:i + 26][-1]


def encryption_weakness(target: int):
    sample = xmas[:xmas.index(target) - 1]
    for size in range(3, len(sample)):
        for start in range(0, len(sample) - size):
            if sum(sample[start:start + size]) == target:
                return max(sample[start:start + size]) + min(sample[start:start + size])


if __name__ == '__main__':

    # --- Solution 1 ---
    print(reconnaissance())  # 85848519
    
    # --- Solution 2 ---
    print(encryption_weakness(85848519))
