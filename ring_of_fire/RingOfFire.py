import random
from .deck import deck


if __name__ == "__main__":
    cards = deck()

    while True:
        try:
            print(random.choice(cards))
            input()
        except KeyboardInterrupt:
            quit()
