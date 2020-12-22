class Player:

    def __init__(self, deck, player_id):
        self.deck = deck
        self.player_id = player_id

    def __len__(self):
        return len(self.deck)

    def draw_card(self):
        return self.deck.pop(0)

    def add_card(self, winning, losing):
        self.deck.append(winning)
        self.deck.append(losing)


def load_game():
    _players = []
    with open('cards.txt', 'r') as file:
        for player_id, line in enumerate(file.read().split('\n\n')):
            deck = [int(x) for x in line.split('\n')[1:]]
            _players.append(Player(deck, player_id))
    return _players


# --- Solution 1 ---

def combat_round(players):
    max_card = -float('inf')
    winner = None
    cards = []
    for player in players:
        draw = player.draw_card()
        if draw > max_card:
            max_card = draw
            winner = player
        cards.append(draw)
    winner.add_card(max_card, min(cards))


def check_winner(players):
    for player in players:
        if len(player) == 0:
            return True, player
    return False, None


def play_combat():
    players = load_game()
    while True:
        is_winner = check_winner(players)
        if not is_winner[0]:
            combat_round(players)
        else:
            break
    winner = [player for player in players if len(player) > 0][0]
    score = 0
    for index, card in enumerate(reversed(winner.deck), 1):
        score += index * card
    return score


print(play_combat())


# --- Solution 2 ---

def recursion_combat(players):
    previous_hands = {}
    while True:
        # --- Check for a repeated configuration ---
        for player in players:
            if player in previous_hands:
                if player.deck in previous_hands[player]:
                    return players[0]
                else:
                    previous_hands[player].append(player.deck[:])
            else:
                previous_hands.update({player: [player.deck[:]]})

        # --- Check in one player has won the game (or sub-game) ---
        is_winner = check_winner(players)
        if is_winner[0]:
            return [player for player in players if player != is_winner[1]][0]

        # --- Draw cards and check whether card value equals the length of the remaining cards ---
        cards = []
        subgame_start = []
        for player in players:
            draw = player.draw_card()
            cards.append((draw, player))
            subgame_start.append(draw <= len(player))

        # --- Enter sub-game if all conditions met, else play regular combat ---
        if all(subgame_start):
            sub_players = []
            for card, player in cards:  # Possibly duplicate
                sub_players.append(Player(player.deck[:card], player.player_id))
            winner = recursion_combat(sub_players)
        else:
            max_card = -float('inf')
            winner = None
            for card, player in cards:
                if card > max_card:
                    max_card = card
                    winner = player

        # --- Add cards to the winner of either round ---
        for card, player in cards:
            if player.player_id == winner.player_id:
                winning = card
                prizewinner = player
            else:
                losing = card
        prizewinner.add_card(winning, losing)


def play_recursion_combat():
    players = load_game()
    winner = recursion_combat(players)
    score = 0
    for index, card in enumerate(reversed(winner.deck), 1):
        score += index * card
    return score


print(play_recursion_combat())
