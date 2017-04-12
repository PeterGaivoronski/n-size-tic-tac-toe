from .random_ai import computer_turn as random_fallback_computer_turn

def close_to_winning(symbol, game_state):
	num_squares = len(game_state["board"])
	diag_0_win = num_squares
	diag_1_win = num_squares
	diag_0_index = 0
	diag_1_index = num_squares - 1
	col_wins = [num_squares for x in game_state["board"][0]]
	row_wins = [num_squares for y in game_state["board"]]

	for y_index, y in enumerate(game_state["board"]):
		for x_index, x in enumerate(y):
			if x == symbol:
				row_wins[y_index] -= 1
				col_wins[x_index] -= 1
				if x_index == diag_0_index:
					diag_0_win -= 1
				if x_index == diag_1_index:
					diag_1_win -= 1

		diag_0_index += 1
		diag_1_index -= 1

	return diag_0_win, diag_1_win, col_wins, row_wins

def place_at_column(col_num, game_state):
	for y_index, y in enumerate(game_state["board"]):
		if game_state["board"][y_index][col_num] == game_state["empty"]:
			game_state["board"][y_index][col_num] = game_state["cpu_symbol"]
			return True
	return False

def place_at_row(row_num, game_state):
	for x_index, x in enumerate(game_state["board"][row_num]):
		if x == game_state["empty"]:
			game_state["board"][row_num][x_index] = game_state["cpu_symbol"]
			return True
	return False

def place_at_diag(diag, game_state):
	if diag == 0:
		diag_index = 0
	else:
		diag_index = len(game_state["board"])-1

	for y_index, y in enumerate(game_state["board"]):
		for x_index, x in enumerate(y):
			if x_index == diag_index and x == game_state["empty"]:
				game_state["board"][y_index][x_index] = game_state["cpu_symbol"]
				return True
		if diag == 0:
			diag_index += 1
		else:
			diag_index -= 1
	return False

def place_potential_win_location(game_state, diag_0_win, diag_1_win, col_wins, row_wins):
	if diag_0_win == 1:
		placed = place_at_diag(0, game_state)
		if placed:
			return True
	if diag_1_win == 1:
		placed = place_at_diag(1, game_state)
		if placed:
			return True
	for col, val in enumerate(col_wins):
		if val == 1:
			placed = place_at_column(col, game_state)
			if placed:
				return True
	for row, val in enumerate(row_wins):
		if val == 1:
			placed = place_at_row(row, game_state)
			if placed:
				return True

	return False

def computer_turn(game_state):
	# If the cpu has 1 left to win a particular case, score it
	placed = place_potential_win_location(game_state, *close_to_winning(game_state["cpu_symbol"], game_state))
	if placed:
		return

	# If the player has 1 left to win a particular case, block it
	placed = place_potential_win_location(game_state, *close_to_winning(game_state["user_symbol"], game_state))
	if placed:
		return
	
	# Player not close to winning, random move
	return random_fallback_computer_turn(game_state)
