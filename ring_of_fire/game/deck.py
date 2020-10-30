
SUIT = ["S", "H", "D", "C"]
RANK = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def deck():

    cards = []

    for suit in SUIT:
        for rank in RANK:
            cards.append(rank+suit)

    return cards
