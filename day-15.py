class MemoryGame:

    def __init__(self):
        self._file = None

    def __enter__(self):
        self._file = open('inputs/game.txt', 'r')
        return self._file.read().split(',')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    @staticmethod
    def play(end: int, starting_numbers: list):
        spoken = {}
        turn = 1
        while turn <= end:
            if turn <= len(starting_numbers):
                if turn == 1:
                    last = int(starting_numbers[0])
                    turn += 1
                    continue
                else:
                    current = int(starting_numbers[turn - 1])
                    last = int(starting_numbers[turn - 2])
            else:
                if last in spoken:
                    current = turn - 1 - spoken[last]
                else:
                    current = 0
            spoken.update({last: turn - 1})
            last = current
            turn += 1
        print(last)


with MemoryGame() as initial_numbers:
    MemoryGame().play(2020, initial_numbers)
    MemoryGame().play(30000000, initial_numbers)
