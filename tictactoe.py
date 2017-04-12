#!/usr/bin/env python

from random import choice

from ai_modules import random_ai, block_and_score_ai

ai_module_map = {
	"random": random_ai,
	"block_and_score": block_and_score_ai
}

input_prompt = "> "

game_state = {"empty": "_"}

def start_game():
	print("let's play tic tac toe")
	print("how many rows/columns?")
	length_entered = False
	while not length_entered:
		try:
			n = int(raw_input(input_prompt))
			if n < 3:
				raise ValueError
			length_entered = True
		except ValueError:
			print("please type an integer more than 2")
	game_state["grid_size"] = 1
	ndiv = n-1
	while ndiv > 9:
		ndiv /= 10
		game_state["grid_size"] += 1
	game_state["grid_midpoint"] = game_state["grid_size"] / 2
	if game_state["grid_size"] % 2 == 0:
		game_state["grid_midpoint"] -= 1
	print("grid_size: {} midpoint: {}".format(game_state["grid_size"], game_state["grid_midpoint"]))
	print("do you want X or O?")
	user_symbol_entered = False
	while not user_symbol_entered:
		user_symbol = raw_input(input_prompt)
		if user_symbol not in {"X", "O"}:
			print("please enter X or O")
		else:
			user_symbol_entered = True
	user_ai_entered = False
	available_ai_modules = ai_module_map.keys()
	ai_message = "please enter one of the following ai modules (or press ENTER for random pick): {}".format(available_ai_modules)
	print(ai_message)
	while not user_ai_entered:
		ai_module = raw_input(input_prompt)
		if ai_module == "":
			ai_module = choice(available_ai_modules)
		if ai_module not in ai_module_map:
			print(ai_message)
		else:
			user_ai_entered = True
	game_state["ai_module"] = ai_module_map[ai_module]
	if user_symbol == "X":
		cpu_symbol = "O"
	else:
		cpu_symbol = "X"
	game_state["user_symbol"] = user_symbol
	game_state["cpu_symbol"] = cpu_symbol
	game_state["board"] = create_board(n)
	print("starting new game with {} rows/columns. ai module: {}".format(n, ai_module))
	game_state["winner"] = None
	if game_state["user_symbol"] == "O":
		# computer goes first
		computer_turn(game_state)
	while game_state["winner"] is None:
		render_game()
		
		game_turn()
		available_idxs = available_spaces()
		game_state["winner"] = evaluate_game()
		if game_state["winner"] is not None:
			break

		available_idxs = available_spaces()
		if check_board_full(available_idxs):
			game_state["winner"] = "neither"
			break
		
		computer_turn(game_state)
		game_state["winner"] = evaluate_game()
		if game_state["winner"] is not None:
			break

		available_idxs = available_spaces()
		if check_board_full(available_idxs):
			game_state["winner"] = "neither"
			break

	render_game()
	if game_state["winner"] == "player":
		print("YOU WIN!")
	elif game_state["winner"] == "cpu":
		print("COMPUTER WINS!")
	else:
		print("TIE GAME!")

def create_board(n):
	return [[game_state["empty"] for x in xrange(n)] for y in xrange(n)]

def game_turn():
	print("enter x,y coords of your next move")
	user_turn_entered = False
	while not user_turn_entered:
		xycoords = str(raw_input(input_prompt))
		try:
			x,y = xycoords.split(",")
			x = int(x)
			y = int(y)
			if game_state["board"][y][x] != game_state["empty"]:
				print("not a valid location")
			else:
				user_turn_entered = True
		except ValueError:
			print("please enter x,y numbers like this: 1,2")
		except IndexError:
			print("your turn is out of bounds")

	game_state["board"][y][x] = game_state["user_symbol"]

def available_spaces():
	available_idxs = []

	for y_index, y in enumerate(game_state["board"]):
		if game_state["empty"] in y:
			y_tuple = (y_index, [])

			for x_index, x in enumerate(y):
				if x == game_state["empty"]:
					y_tuple[1].append(x_index)

			available_idxs.append(y_tuple)

	return available_idxs

def check_board_full(available_idxs):
	if len(available_idxs) == 0:
		return True
	return False

def computer_turn(game_state):
	game_state["ai_module"].computer_turn(game_state)

def evaluate_game():
	p_diag_0_win = True
	c_diag_0_win = True
	p_diag_1_win = True
	c_diag_1_win = True
	diag_0_index = 0
	diag_1_index = len(game_state["board"])-1
	p_col_win = [True for x in game_state["board"][0]]
	c_col_win = [True for x in game_state["board"][0]]

	p_row_win = [True for y in game_state["board"]]
	c_row_win = [True for y in game_state["board"]]

	# print(p_row_win)

	for y_index, y in enumerate(game_state["board"]):
		for x_index, x in enumerate(y):
			player_x = x == game_state["user_symbol"]
			cpu_x = x == game_state["cpu_symbol"]

			if p_row_win[y_index] == True and not player_x:
				p_row_win[y_index] = False
			if c_row_win[y_index] == True and not cpu_x:
				c_row_win[y_index] = False

			if p_col_win[x_index] == True and not player_x:
				p_col_win[x_index] = False
			if c_col_win[x_index] == True and not cpu_x:
				c_col_win[x_index] = False

			if x_index == diag_0_index:
				if p_diag_0_win and not player_x:
					p_diag_0_win = False
				if c_diag_0_win and not cpu_x:
					c_diag_0_win = False
			if x_index == diag_1_index:
				if p_diag_1_win and not player_x:
					p_diag_1_win = False
				if c_diag_1_win and not cpu_x:
					c_diag_1_win = False

		diag_0_index += 1
		diag_1_index -= 1

	if True in p_row_win or p_diag_0_win or p_diag_1_win or True in p_col_win:
		return "player"
	if True in c_row_win or c_diag_0_win or c_diag_1_win or True in c_col_win:
		return "cpu"
	return None

def pad_string(s, spaces):
	padding = spaces - len(s)
	for i in xrange(padding):
		s += " "
	return s

def render_game():
	string = ""
	x_index = 0
	string += pad_string("", game_state["grid_size"])
	string += "|"
	for x in game_state["board"][0]:
		string += pad_string(str(x_index), game_state["grid_size"])
		string += "|"
		x_index += 1
	string = string[:-1] + "\n"
	y_index = 0
	for y in game_state["board"]:
		string += pad_string(str(y_index), game_state["grid_size"])+"|"
		y_index += 1
		for x in y:
			for i in xrange(game_state["grid_size"]):
				if i == game_state["grid_midpoint"]:
					string += x
				else:
					string += game_state["empty"]
			string += "|"

		string = string[:-1] + "\n"
	print(string)

while True:
	start_game()