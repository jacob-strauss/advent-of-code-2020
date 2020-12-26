class Item:

    def __init__(self, public_key, subject):
        self.public_key = public_key
        self.subject = subject
        self.loop_size = 1

    def handshake(self, value=1, subject=7):
        for _ in range(self.loop_size):
            value *= subject
            value = value % 20201227
        return value


def determine_loop_size(item: Item):
    loop_size = 1
    value = 1
    while True:
        value *= item.subject
        value = value % 20201227
        if value == item.public_key:
            item.loop_size = loop_size
            break
        loop_size += 1


def load_file():
    with open('inputs/keys.txt', 'r') as file:
        return file.read().split('\n')


def determine_encryption_key():
    public_keys = load_file()
    card = Item(int(public_keys[0]), 7)
    door = Item(int(public_keys[1]), 7)
    determine_loop_size(card)
    determine_loop_size(door)
    print(card.loop_size)
    print(door.loop_size)
    return door.handshake(subject=card.public_key)


print(determine_encryption_key())
