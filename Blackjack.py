import random
from Cards import *
from time import sleep
from Colours import colours


def print_square(message, colour, is_double=False):
    top_left = "┌" if not is_double else "╔"
    top_right = "┐" if not is_double else "╗"
    bottom_left = "└" if not is_double else "╚"
    bottom_right = "┘" if not is_double else "╝"
    horizontal = "─" if not is_double else "═"
    vertical = "│" if not is_double else "║"

    print(colour, end="")  # set colour
    print(f"{top_left}{horizontal}{horizontal * len(message)}{horizontal}{top_right}")
    print(f"{vertical} {message} {vertical}")
    print(f"{bottom_left}{horizontal}{horizontal * len(message)}{horizontal}{bottom_right}")
    print(colours['reset'], end="")  # reset colour


def prompt_player_hit():
    response = None

    while response not in ['Y', 'N']:
        response = input(f"{colours['cyan']}Hit? Y/N > {colours['reset']}").upper()

    return True if response == 'Y' else False


results = {
    'player_wins': 0,
    'dealer_wins': 0,
    'nobody_wins': 0,
    'push': 0,
}


def print_results():
    print(f"{colours['green']}Player wins: {results['player_wins']}")
    print(f"{colours['red']}Dealer wins: {results['dealer_wins']}")
    print(f"{colours['gray']}Nobody wins: {results['nobody_wins']}")
    print(f"{colours['cyan']}Pushes     : {results['push']}")
    print(colours['reset'], end='')


def main():
    # Shuffle the cards
    random.shuffle(cards)

    player_hand = []
    dealer_hand = []

    # Round 1
    # deal player 1 card face up
    # deal dealer 1 card face up
    print_square("Dealing first cards...", colours['yellow'])
    print()
    sleep(0.5)

    deal(cards, player_hand)
    print_cards(player_hand, "Player")

    deal(cards, dealer_hand)
    print_cards(dealer_hand, "Dealer")

    # Round 2
    # deal player 1 card face up
    # deal dealer 1 card face down
    sleep(0.5)
    print_square("Dealing second cards...", colours['yellow'])
    print()
    sleep(0.5)

    deal(cards, player_hand)
    print_cards(player_hand, "Player")

    deal(cards, dealer_hand)
    print_cards(dealer_hand, "Dealer", True)

    # Round 3+
    # player may choose to hit or stand
    player_lost = False
    player_21 = get_hand_total(player_hand) == 21

    while prompt_player_hit():
        print()
        print_square("Hitting...", colours['yellow'])
        print()
        sleep(0.5)

        deal(cards, player_hand)
        print_cards(player_hand, "Player")
        print_cards(dealer_hand, "Dealer", True)

        if get_hand_total(player_hand) == 21:
            player_21 = True
            break
        elif get_hand_total(player_hand) > 21:
            player_lost = True
            break

    if player_21:
        print_square("Player's hand totals 21", colours['cyan'])
    elif player_lost:
        print_square("Player's hand exceeds 21", colours['red'])

    print()
    sleep(0.5)
    print_square("Revealing dealer's card...", colours['yellow'])
    sleep(0.5)
    print()
    print_cards(player_hand, "Player")
    print_cards(dealer_hand, "Dealer")

    while get_hand_total(dealer_hand) < 17:
        sleep(0.5)
        print_square("Dealer's hand less than 17. Hitting...", colours['yellow'])
        print()
        sleep(0.5)
        deal(cards, dealer_hand)
        print_cards(player_hand, "Player")
        print_cards(dealer_hand, "Dealer")

    player_total = get_hand_total(player_hand)
    dealer_total = get_hand_total(dealer_hand)

    # Determine winner
    if player_total == 21 and dealer_total == 21:
        # If dealer has blackjack and player doesn't, dealer wins
        if len(dealer_hand) == 2 and len(player_hand) > 2:
            print_square("Dealer wins", colours['red'], True)
            results['dealer_wins'] += 1
        # If player has blackjack and dealer doesn't, player wins
        elif len(player_hand) == 2 and len(dealer_hand) > 2:
            print_square("Player wins", colours['green'], True)
            results['player_wins'] += 1
        # If neither player nor dealer has blackjack or both have blackjack, it's a push
        else:
            print_square("Push", colours['cyan'], True)
            results['push'] += 1
    # Both bust
    elif player_total > 21 and dealer_total > 21:
        print_square("Nobody wins", colours['gray'], True)
        results['nobody_wins'] += 1
    # Both have same score less than 21
    elif player_total == dealer_total:
        print_square("Push", colours['cyan'], True)
        results['push'] += 1
    # Dealer not bust and higher score than player, dealer wins
    # Dealer not bust and player bust, dealer wins
    elif (player_total < dealer_total <= 21) or (dealer_total <= 21 < player_total):
        print_square("Dealer wins", colours['red'], True)
        results['dealer_wins'] += 1
    # Player not bust and higher score than dealer, player wins
    # Player not bust and dealer bust, player wins
    elif (dealer_total < player_total <= 21) or (player_total <= 21 < dealer_total):
        print_square("Player wins", colours['green'], True)
        results['player_wins'] += 1
    else:
        print('UNHANDLED - Logic error if this is reached')


if __name__ == "__main__":
    main()


    def prompt_play_again():
        response = None

        while response not in ['Y', 'N']:
            response = input(f"\n{colours['cyan']}Play again? Y/N > {colours['reset']}").upper()

        return True if response == 'Y' else False

    while prompt_play_again():
        print()
        main()

    print('\nThanks for playing!')
    print('Here are the results from this session:\n')
    print_results()
    print('\nGoodbye!')
