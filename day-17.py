from itertools import product


def neighbouring_space(cube):
    for x, y, z, w in product([0, 1, -1], repeat=4):
        if not x == y == z == w == 0:
            yield cube.coordinate[0] + x, cube.coordinate[1] + y, cube.coordinate[2] + z, cube.coordinate[3] + w

    # --- For Solution 1 ---

    # for x, y, z in product([0, 1, -1], repeat=3):
    #     if not x == y == z == 0:
    #         yield cube.coordinate[0] + x, cube.coordinate[1] + y, cube.coordinate[2] + z


class Cube:

    def __init__(self, coordinate: tuple, active: bool):
        self.coordinate = coordinate
        self.active = active
        self.neighbours = []

    def remove_neighbour(self, cube):
        self.neighbours.remove(cube)

    def has_active_neighbour(self):
        for neighbour in self.neighbours:
            if neighbour.active:
                return True
        return False


class Space:

    def __init__(self):
        self.cubes = []

    def __len__(self):
        return len([cube for cube in self.cubes if cube.active])

    def remove_inactive_cubes(self):
        for cube in self.cubes[:]:
            if not cube.active:
                if not cube.has_active_neighbour():
                    for neighbour in cube.neighbours:
                        neighbour.remove_neighbour(cube)
                    self.cubes.remove(cube)

    def add_cubes(self):
        for cube in self.cubes[:]:
            if cube.active:
                if len(cube.neighbours) != 80:  # For Solution 1 change to 26
                    n_coors = [n.coordinate for n in cube.neighbours]
                    for n_space in neighbouring_space(cube):
                        if n_space not in n_coors:
                            new_cube = Cube(coordinate=tuple(n_space), active=False)
                            self.link_neighbours(new_cube)
                            self.cubes.append(new_cube)

    def link_neighbours(self, new_cube: Cube):
        n_space = [n for n in neighbouring_space(new_cube)]
        for cube in self.cubes:
            if cube.coordinate in n_space:
                cube.neighbours.append(new_cube)
                new_cube.neighbours.append(cube)

    def cycle(self):
        self.remove_inactive_cubes()
        self.add_cubes()
        change_active = []
        change_inactive = []
        for i, cube in enumerate(self.cubes):
            if cube.active:
                if not 1 < len([n for n in cube.neighbours if n.active]) < 4:
                    change_inactive.append(i)
            else:
                if len([n for n in cube.neighbours if n.active]) == 3:
                    change_active.append(i)
        for index in change_active:
            self.cubes[index].active = True
        for index in change_inactive:
            self.cubes[index].active = False


def load_state():
    with open('inputs/conway.txt', 'r') as file:
        initial_state = Space()
        for y, row in enumerate(reversed(file.readlines())):
            for x, elem in enumerate(row.strip()):
                if elem == '.':
                    new_cube = Cube(coordinate=(x, y, 0, 0), active=False)  # For Solution 1 change to (x, y, z)
                else:
                    new_cube = Cube(coordinate=(x, y, 0, 0), active=True)
                initial_state.link_neighbours(new_cube)
                initial_state.cubes.append(new_cube)
    return initial_state


space = load_state()

for _ in range(6):
    space.cycle()

print(len(space))
