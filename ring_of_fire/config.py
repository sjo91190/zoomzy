

def card_actions(card, name):

	actions = {
		"A": f"Waterfall! Everyone drink and don't stop until {name} is finished!",
		"2": f"{name} gets to choose someone to take a drink with"

	}

	return actions.get(card)
