with open('instructions.txt', 'r') as file:
    boot_code = file.readlines()


# --- Solution 1 ---

def run_code(code):
    visited = []
    acc = 0
    i = 0

    while i not in visited:
        if i >= len(code):
            return True, acc
        visited.append(i)
        op, arg = code[i].split()
        if op == 'jmp':
            i += int(arg) - 1
        elif op == 'acc':
            acc += int(arg)
        i += 1

    return False, acc


# --- Solution 2 ---

def fix_code():
    for index, line in enumerate(boot_code):
        op, arg = line.split()
        if op == 'acc':
            continue
        code_copy = boot_code[:]
        if op == 'jmp':
            code_copy[index] = f"nop {arg}"
        else:
            code_copy[index] = f"jmp {arg}"

        res, acc = run_code(code_copy)
        if res:
            return acc
