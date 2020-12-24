from copy import deepcopy
import re


# --- Solution 1 ---

def tile_location():
    with open('inputs/tiles.txt', 'r') as file:
        for line in file.readlines():
            se = len(re.findall(r'se', line))
            sw = len(re.findall(r'sw', line))
            nw = len(re.findall(r'nw', line))
            ne = len(re.findall(r'ne', line))
            e = len(re.findall(r'e', line))
            w = len(re.findall('w', line))

            directions = {'ne': ne - sw, 'e': (e - ne - se) - (w - nw - sw), 'se': se - nw}

            if directions['ne'] < 0 and directions['se'] < 0:
                largest = abs(max(directions['ne'], directions['se']))
                directions['ne'] += largest
                directions['se'] += largest
                directions['e'] -= largest
            elif directions['ne'] > 0 and directions['se'] > 0:
                smallest = min(directions['ne'], directions['se'])
                directions['ne'] -= smallest
                directions['se'] -= smallest
                directions['e'] += smallest

            if directions['e'] < 0 and directions['ne'] > 0:
                smallest = min(abs(directions['e']), directions['ne'])
                directions['ne'] -= smallest
                directions['e'] += smallest
                directions['se'] -= smallest
            if directions['e'] > 0 and directions['se'] < 0:
                smallest = min(directions['e'], abs(directions['se']))
                directions['se'] += smallest
                directions['e'] -= smallest
                directions['ne'] += smallest
            if directions['e'] > 0 and directions['ne'] < 0:
                smallest = min(directions['e'], abs(directions['ne']))
                directions['e'] -= smallest
                directions['ne'] += smallest
                directions['se'] += smallest
            if directions['e'] < 0 and directions['se'] > 0:
                smallest = min(abs(directions['e']), directions['se'])
                directions['e'] += smallest
                directions['se'] -= smallest
                directions['ne'] -= smallest

            yield directions['ne'], directions['e'], directions['se']


def determine_colour():
    tiles = {}
    for tile in tile_location():
        if tile in tiles:
            tiles[tile] += 1
        else:
            tiles.update({tile: 1})

    black = 0
    white = 0
    for flips in tiles.values():
        if flips % 2 == 0:
            white += 1
        else:
            black += 1

    return black, white


# print(determine_colour())


# --- Solution 2 ---


class Tile:

    def __init__(self, coordinate, black):
        self.coordinate = coordinate
        self.black = black

    def neighbour_coors(self):
        for ne, e, se in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)):
            yield self.coordinate[0] + ne, self.coordinate[1] + e, self.coordinate[2] + se


class Lobby:

    def __init__(self):
        self.tiles = {}
        self._get_tiles()

    def __len__(self):
        black_tiles = 0
        for tile in self.tiles.values():
            if tile.black:
                black_tiles += 1
        return black_tiles

    @staticmethod
    def simplify_coordinate(coordinate: tuple):
        """
        :param coordinate: A tuple in the format (ne, e, se)
        :return: Simplified coordinate value
        """
        ne, e, se = coordinate
        if ne < 0 and se < 0:
            largest = abs(max(ne, se))
            ne += largest
            se += largest
            e -= largest
        elif ne > 0 and se > 0:
            smallest = min(ne, se)
            ne -= smallest
            se -= smallest
            e += smallest
        if e < 0 and ne > 0:
            smallest = min(abs(e), ne)
            ne -= smallest
            e += smallest
            se -= smallest
        if e > 0 and se < 0:
            smallest = min(e, abs(se))
            se += smallest
            e -= smallest
            ne += smallest
        if e > 0 and ne < 0:
            smallest = min(e, abs(ne))
            e -= smallest
            ne += smallest
            se += smallest
        if e < 0 and se > 0:
            smallest = min(abs(e), se)
            e += smallest
            se -= smallest
            ne -= smallest

        return ne, e, se

    def _get_tiles(self):
        with open('inputs/tiles.txt', 'r') as file:
            for line in file.readlines():
                path = ''
                for char in line.strip():
                    if char == 'n' or char == 's':
                        path += char
                    else:
                        path += char
                        se = len(re.findall(r'se', path))
                        sw = len(re.findall(r'sw', path))
                        nw = len(re.findall(r'nw', path))
                        ne = len(re.findall(r'ne', path))
                        e = len(re.findall(r'e', path))
                        w = len(re.findall('w', path))
                        coordinate = self.simplify_coordinate((ne - sw, (e - ne - se) - (w - nw - sw), se - nw))
                        if coordinate in self.tiles:
                            continue
                        else:
                            self.tiles.update({coordinate: Tile(coordinate=coordinate, black=False)})
                self.tiles[coordinate].black = not self.tiles[coordinate].black


def exhibition():
    lobby = Lobby()
    for i in range(100):
        temp = deepcopy(lobby.tiles)
        for location, tile in temp.items():
            adjacent = 0
            if tile.black:
                for neighbour_coord in tile.neighbour_coors():
                    neighbour = lobby.simplify_coordinate(neighbour_coord)
                    if neighbour in temp:
                        if temp[neighbour].black:
                            adjacent += 1
                    else:
                        new_tile = Tile(coordinate=neighbour, black=False)
                        new_adjacent = 0
                        for new_coordinate in new_tile.neighbour_coors():
                            new_neighbour = lobby.simplify_coordinate(new_coordinate)
                            if new_neighbour in temp:
                                if temp[new_neighbour].black:
                                    new_adjacent += 1
                        if new_adjacent == 2:
                            new_tile.black = True
                        lobby.tiles.update({neighbour: new_tile})
                if 0 < adjacent < 3:
                    continue
                else:
                    lobby.tiles[location].black = False
            else:
                for neighbour_coord in tile.neighbour_coors():
                    neighbour = lobby.simplify_coordinate(neighbour_coord)
                    if neighbour in temp:
                        if temp[neighbour].black:
                            adjacent += 1
                if adjacent == 2:
                    lobby.tiles[location].black = True
    return len(lobby)


print(exhibition())
