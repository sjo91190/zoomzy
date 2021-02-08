import random
from app.ring_of_fire.utils.deck import deck


def shuffle(card_deck):

    card_deck.extend(deck())


def random_card(card_deck):

    if len(card_deck) == 0:
        return "END OF DECK"

    card = random.choice(card_deck)
    card_deck.remove(card)

    return card


def top_pop(config_dict):

    card_num = config_dict["POP"]
    true_weight = 0
    false_weight = 1

    if card_num >= 15:
        false_weight = (52 - card_num) / 100
        true_weight = 1 - false_weight

    will_pop = random.choices(population=[True, False], weights=[true_weight, false_weight], k=1)
    config_dict["POP"] += 1

    if will_pop[0]:
        config_dict["POP"] = 0
        pass

    return will_pop[0]


def next_player(index, count):
    count -= 1
    if index < count:
        return index + 1

    return 0
