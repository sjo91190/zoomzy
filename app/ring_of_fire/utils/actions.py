

def card_actions(card, name):

    _actions = {
        "A": f"Waterfall! everyone drink and don't stop until {name} is finished!",
        "2": f"{name} gets to choose someone to take a drink with",
        "3": f"{name}... drink up, buddy",
        "4": "LADIES! drink your drink!!",
        "5": f"""{name} is now the Thumb Master. 
        put a thumb up on screen at any time and the last to put their thumb up drinks""",
        "6": "FELLAS! drink your drink",
        "7": f"{name}, flick off the camera. Last to return the bird drinks!",
        "8": f"{name}, choose a partner that will have to drink every time you do",
        "9": f"""Rhyme time! {name}, say a word and then the next player has to say a word
        that rhymes. This continues until someone fails.. and they drink""",
        "1": f"""Categories! {name}, name a category. The next person needs to say a word 
        that fits the category. If you can't deliver, you DRINK!!""",
        "J": "Never Have I Ever! Those that have ever, drink up!",
        "Q": f"""Question Master! {name}, until another player pulls this card, you may
        ask any player a question, and if they don't answer with a question, they drink.
        If you don't answer their question""",
        "K": f"{name} gets to create a rule that lasts until the game ends!"
    }

    return _actions.get(card)
