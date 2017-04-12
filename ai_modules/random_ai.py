from random import choice

def available_spaces(game_state):
	available_idxs = []

	for y_index, y in enumerate(game_state["board"]):
		if "_" in y:
			y_tuple = (y_index, [])

			for x_index, x in enumerate(y):
				if x == "_":
					y_tuple[1].append(x_index)

			available_idxs.append(y_tuple)

	return available_idxs

def computer_turn(game_state):
	r_choice = choice(available_spaces(game_state))
	y = r_choice[0]
	x = choice(r_choice[1])

	game_state["board"][y][x] = game_state["cpu_symbol"] 
