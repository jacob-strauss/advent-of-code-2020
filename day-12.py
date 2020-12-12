def navigation(path):
    with open(path, 'r') as file:
        for row in file:
            yield row[0], int(row[1:])


class Ship:

    def __init__(self, waypoint):
        self.position = complex(0, 0)
        self.waypoint = waypoint

    def __str__(self):
        return str(abs(self.position.real) + abs(self.position.imag))

    def rotate(self, direction, angle):
        if direction == 'R':
            angle = 360 - angle
        for _ in range(angle // 90):
            self.waypoint = complex(-self.waypoint.imag, self.waypoint.real)

    def move(self, direction, magnitude, move_waypoint):
        if move_waypoint:
            self.waypoint += direction * magnitude
        else:
            self.position += direction * magnitude

    def steer_ship(self, direction, magnitude, from_waypoint):
        if direction == 'N':
            self.move(complex(0, 1), magnitude, from_waypoint)
        elif direction == 'S':
            self.move(complex(0, -1), magnitude, from_waypoint)
        elif direction == 'E':
            self.move(complex(1, 0), magnitude, from_waypoint)
        elif direction == 'W':
            self.move(complex(-1, 0), magnitude, from_waypoint)
        elif direction == 'F':
            self.move(self.waypoint, magnitude, False)
        else:
            self.rotate(direction, magnitude)


# --- Solution 1 ---

ship_1 = Ship(waypoint=complex(1, 0))
for direct, value in navigation('inputs/navigation.txt'):
    ship_1.steer_ship(direct, value, False)

print(ship_1)

# --- Solution 2 ---

ship_2 = Ship(waypoint=complex(10, 1))
for direct, value in navigation('inputs/navigation.txt'):
    ship_2.steer_ship(direct, value, True)

print(ship_2)