from Colours import colours

suits = ['\u2660', '\u2663', '\u2665', '\u2666']
ace_card = 'A'
face_cards = ['J', 'Q', 'K']
number_cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
names = [ace_card] + number_cards + face_cards

# Generate deck
cards = []
for suit in suits:
    for name in names:
        if name == ace_card:
            value = 11
        elif name in face_cards:
            value = 10
        else:
            value = int(name)

        cards.append({
            'name': name,
            'suit': suit,
            'value': value,
        })


def get_deck():
    return cards.copy()


def deal(cards, hand):
    hand.append(cards.pop())


def get_hand_total(hand):
    total = 0
    aces = 0

    for card in hand:
        if card['name'] == ace_card:
            aces += 1
        else:
            total += card['value']

    if aces > 0:
        if 21 - (aces - 1) - total >= 11:
            total += 11 + (aces - 1)
        else:
            total += aces

    return total


def print_cards(hand, name, hide_dealer=False):
    lines = ['', '', '', '', '']

    face_down_card = [
        "┌┬┬┬┬┬┐",
        "│┆┆┆┆┆│",
        "│┆┆┆┆┆│",
        "│┆┆┆┆┆│",
        "└┴┴┴┴┴┘",
    ]

    def append_card(card, lines):
        lines[0] += '┌─────┐'

        lines[1] += f"│{card['name']}   "
        if len(card['name']) < 2:
            lines[1] += ' '
        lines[1] += '│'

        lines[2] += f"│  {card['suit']}  │"

        lines[3] += '│ '
        if len(card['name']) < 2:
            lines[3] += ' '
        lines[3] += f"  {card['name']}│"

        lines[4] += '└─────┘'

    if hide_dealer:
        append_card(hand[0], lines)
        for i in range(len(lines)):
            lines[i] += face_down_card[i]
    else:
        for card in hand:
            append_card(card, lines)

    print(f"{name}:")

    for line in lines:
        print(line)

    print(colours['green'], end="")  # set green
    if hide_dealer:
        print(f"Total: {hand[0]['value']} + ?\n")
    else:
        total = get_hand_total(hand)
        blackjack = total == 21 and len(hand) == 2
        message = f"Total: {total}{' (Blackjack!)' if blackjack else ''}\n"
        print(message)
    print(colours['reset'], end="")  # reset
