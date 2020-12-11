from copy import deepcopy

with open('inputs/seats.txt', 'r') as file:
    seats = [list(x.strip()) for x in file.readlines()]


def spaces():
    for y in range(len(seats)):
        for x in range(len(seats[0])):
            yield y, x


def on_grid(y: int, x: int):
    return 0 <= y < len(seats) and 0 <= x < len(seats[0])


# --- Solution 1 ---


def adjacent_cells(y: int, x: int):
    for i, j in ((-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1), (1, -1)):
        yield y + j, x + i


def check_seats(seat_map):
    new_layout = deepcopy(seat_map)
    for y, x in spaces():
        if seat_map[y][x] == '.':
            continue
        occupied_seats = 0
        for j, i in adjacent_cells(y, x):
            if on_grid(j, i):
                if seat_map[j][i] == '#':
                    occupied_seats += 1
        if seat_map[y][x] == 'L':
            if occupied_seats == 0:
                new_layout[y][x] = '#'
        else:
            if occupied_seats >= 4:
                new_layout[y][x] = 'L'
    if new_layout == seat_map:
        return sum(map(lambda l: l.count('#'), new_layout))
    return check_seats(new_layout)


# --- Solution 2 ---


def adjacent_indexes():
    for i, j in ((-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1), (1, -1)):
        yield j, i


def check_visible(seat_map):
    new_layout = deepcopy(seat_map)
    for y, x in spaces():
        if seat_map[y][x] == '.':
            continue
        occupied_seats = 0
        for j, i in adjacent_indexes():
            b = y
            a = x
            while on_grid(b + j, a + i):
                b += j
                a += i
                if seat_map[b][a] == '.':
                    continue
                elif seat_map[b][a] == '#':
                    occupied_seats += 1
                    break
                else:
                    break
        if seat_map[y][x] == 'L':
            if occupied_seats == 0:
                new_layout[y][x] = '#'
        else:
            if occupied_seats >= 5:
                new_layout[y][x] = 'L'
    if new_layout == seat_map:
        return sum(map(lambda l: l.count('#'), new_layout))
    return check_visible(new_layout)
