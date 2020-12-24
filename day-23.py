# --- Solution 1 ---

class CrabCups:

    def __init__(self):
        self.cups = []
        self.pickup = []
        self.current = 0
        self._load_game()

    def __str__(self):
        ordered_cups = ''
        start = self.cups.index(1)
        for i in range(1, len(self.cups)):
            ordered_cups += str(self.cups[(start + i) % len(self.cups)])
        return ordered_cups

    def _load_game(self):
        with open('inputs/cups.txt', 'r') as file:
            self.cups = [int(cup) for cup in file.read()]
        self.current = self.cups[0]

    def pickup_cups(self):
        current_index = self.cups.index(self.current)  # Too slow - use linked lists
        for i in range(1, 4):
            cup = self.cups[(current_index + i) % len(self.cups)]
            self.pickup.append(cup)
        for cup in self.pickup:
            self.cups.remove(cup)

    def place_cups(self, element):
        index = self.cups.index(element) + 1  # Too slow find element through linked list
        self.cups[index:index] = self.pickup

    def destination_cup(self):
        destination = None
        temp = self.current
        minimum = min(self.cups)
        while destination is None:
            temp -= 1
            if temp < minimum:
                destination = max(self.cups)
            else:
                if temp in self.cups:  # Don't need to check against all cups - just against the removed ones and min
                    destination = temp
        return destination

    def change_current(self):
        index = self.cups.index(self.current) + 1  # Too slow - just go to next node in linked list
        self.current = self.cups[index % len(self.cups)]
        self.pickup = []


def play_crab_cups():
    crab_cups = CrabCups()

    for _ in range(100):
        crab_cups.pickup_cups()
        destination_cup = crab_cups.destination_cup()
        crab_cups.place_cups(destination_cup)
        crab_cups.change_current()

    print(crab_cups)


# --- Solution 2 ---

class Cup:

    def __init__(self, label=None, next_cup=None):
        self.label = label
        self.next_cup = next_cup

    def __str__(self):
        return str(self.label)


class Crab:

    def __init__(self, current=None):
        self.current = current
        self.unlinked = []

    def unlink_cups(self):
        previous_cup = self.current
        for _ in range(3):
            self.unlinked.append(previous_cup.next_cup)
            previous_cup = previous_cup.next_cup
        self.current.next_cup = previous_cup.next_cup
        previous_cup.next_cup = None

    def insert_cups(self, cup: Cup):
        self.unlinked[-1].next_cup = cup.next_cup
        cup.next_cup = self.unlinked[0]
        self.unlinked = []


class CupCircle:

    def __init__(self):
        self.cups = {}
        self.first = 0
        self._arrange_cups()

    def __str__(self):
        result = 1
        cup = self.cups[1]
        for i in range(1, 3):
            result *= cup.next_cup.label
            cup = cup.next_cup
        return str(result)

    @staticmethod
    def _read_file():
        with open('inputs/cups.txt', 'r') as file:
            for label in file.read():
                yield int(label)
        for label in range(10, 1000001):
            yield label

    def _arrange_cups(self):
        labels = self._read_file()
        previous_label = next(labels)
        self.first = previous_label
        previous_cup = Cup(previous_label)
        current_cup = None
        for label in labels:
            current_cup = Cup(label)
            previous_cup.next_cup = current_cup
            self.cups.update({previous_label: previous_cup})
            previous_label = label
            previous_cup = current_cup
        current_cup.next_cup = self.cups[self.first]
        self.cups.update({previous_label: current_cup})


def play_real_crab_cups():
    circle = CupCircle()
    crab = Crab(circle.cups[circle.first])
    for i in range(10000000):
        crab.unlink_cups()
        # --- Find destination cup ---
        destination = None
        unlinked_labels = [cup.label for cup in crab.unlinked]
        current = crab.current.label
        while destination is None:
            current -= 1
            if current == 0:
                current = 1000001  # Needs to be one greater than max value
            elif current not in unlinked_labels:
                destination = current
        destination_cup = circle.cups[destination]
        crab.insert_cups(destination_cup)
        crab.current = crab.current.next_cup
    print(circle)


play_real_crab_cups()  # 42.9 seconds!
