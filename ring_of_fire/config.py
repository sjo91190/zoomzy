

def card_actions(card, name):

	actions = {
		"A": f"Waterfall! Everyone drink and don't stop until {name} is finished!",
		"2": f"{name} gets to choose someone to take a drink with",
		"3": "3",
		"4": "4",
		"5": f"""{name} is now the Thumb Master. 
		Put a thumb up on screen at any time and the last to put their thumb up drinks""",
		"6": "6",
		"7": "7",
		"8": "8",
		"9":"9",
		"1": "10",
		"J": "JACK",
		"Q": "QUEEN",
		"K": f"{name} gets to create a rule that lasts until the game ends!"
	}

	return actions.get(card)
