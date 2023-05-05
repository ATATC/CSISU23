# CSISU23

## Goal

The goal of the project is to create a console-based Tic-Tac-Toe game implemented by *Python*.

## Design

### `tictactoe/__init__.py`

#### `TicTacToeRS.post_piece_down(x, y, p_index)`

| Variable | Type  | Usage        |
| -------- | ----- | ------------ |
| x        | `int` | x-coordinate |
| y        | `int` | y-coordinate |
| p_index  | `int` | piece index  |

```pseudocode
IF this.board.get_round_counter() == board.size THEN RAISE Tied
IF (x + y) % 2 == 0 AND (diagonal_1.count(p_index) == 3 OR diagonal_2.count(p_index) == 3)
	RAISE GameOver
IF row_y.count(p_index) == board.width OR column_x.count(p_index) == board.height
	RAISE GameOver
```

#### `HumanPlayer.decide(board)`

| Variable | Type    | Usage                      |
| -------- | ------- | -------------------------- |
| board    | `Board` | the board                  |
| d        | `str`   | user's decision, 1-D index |

```pseudocode
d = ""
WHILE !decision.isnumeric()
	d = INPUT
RETURN board.revert_index(int(d) - 1)
```

#### `Bot.decide(board)`

| Variable | Type    | Usage                               |
| -------- | ------- | ----------------------------------- |
| board    | `Board` | the board                           |
| opi      | `int`   | opponent's piece index              |
| i        | `int`   | index of the first available corner |
| r        | `tuple` | return coordinates                  |

```pseudocode
IF board.get_round_counter() > 9 THEN RAISE Surrender
IF board.get_round_counter() == 0 THEN RETURN RANDOM_CHOICE(0, 2), RANDOM_CHOICE(0, 2)
opi = 1 - this.p_index
IF board.get_round_counter() > 2
	r = for_each_line(board, this.p_index, opi, defend)
	IF r != null THEN RETURN r
corners = (board[0][0], board[2][0], board[2][2], board[0][2])
IF corners.count(this.p_index) == 3 AND board[1][1] == -1 THEN RETURN 1, 1
i = index(corners, -1)
SWITCH (i)
	CASE 0 THEN RETURN 0, 0
	CASE 1 THEN RETURN 2, 0
	CASE 2 THEN RETURN 2, 2
	CASE 3 THEN RETURN 0, 2
r = for_each_line(board, this.p_index, opi, attack)
IF r == null THEN RAISE Surrender
RETURN r
```

#### `choose_player(serial, p_index, ai_bot)`

| Variable       | Type     | Usage                                       |
| -------------- | -------- | ------------------------------------------- |
| serial         | `str`    | serial of the player, such as "A" or "B"    |
| p_index        | `int`    | the index of the piece that the player uses |
| ai_bot         | `bool`   | enable AI bot                               |
| player         | `Player` | the player object                           |
| rd_dir         | `str`    | the location to save recorded decisions     |
| default_rd_dir | `str`    | default location to save recorded decisions |
| option         | `str`    | human or bot                                |
| name           | `str`    | user's name                                 |

```pseudocode
player = null
rd_dir = null
serial = serial.upper()
default_rd_dir = "./recorded_decisions/" + serial.lower() + ".rd"
WHILE player == null
	option = INPUT
	IF option == "H"
		name = INPUT
		player = HumanPlayer(name == "" ? "Player " + serial : name, p_index)
	ELSE IF option == "B":
		IF ai_bot THEN player = LOAD_AI_BOT
		ELSE player = Bot("Bot " + serial, p_index)
	ELSE PRINT_ERROR_MESSAGE
IF INPUT == "Y"
	rd_dir = INPUT
	IF rd_dir == "" THEN rd_dir = default_rd_dir
	player = ProgrammedPlayer(player, READ_FILE)
	rd_dir = None
ELSE IF INPUT == "Y"
	player.record()
	rd_dir = INPUT
	IF rd_dir == "" THEN rd_dir = default_rd_dir
RETURN player, rd_dir
```

### `tictactoe/framework/board.py`

#### `Board.check_index(x, y, override)`

| Variable | Type   | Usage            |
| -------- | ------ | ---------------- |
| x        | `int`  | x-coordinate     |
| y        | `int`  | y-coordinate     |
| override | `bool` | allow overriding |

```pseudocode
IF x >= this.width OR y >= this.height OR (!override AND this.p_map[y][x] != -1) THEN RAISE InvalidStep
```

#### `Board.go(x, y, p_index, override)`

| Variable | Type   | Usage            |
| -------- | ------ | ---------------- |
| x        | `int`  | x-coordinate     |
| y        | `int`  | y-coordinate     |
| p_index  | `int`  | piece index      |
| override | `bool` | allow overriding |

```pseudocode
this.check_p_index(p_index)
this.rule_set.on_piece_down(x, y, p_index)
this.check_index(x, y, override)
this.p_map[y][x] = p_index
this.round_counter++
this.rule_set.post_piece_down(x, y, p_index)
```

#### `Board.blanks()`

| Variable | Type   | Usage                               |
| -------- | ------ | ----------------------------------- |
| i        | `int`  | loop counter                        |
| r        | `list` | return value, a list of 2-D indexes |
| row      | `list` | a row                               |
| p        | `int`  | piece                               |

```pseudocode
i = 0
r = []
FOR row OF this.p_map
	FOR p OF row
		IF p == -1 THEN r.append(this.revert_index(i))
		i++
RETURN r
```

#### `Board.show_indexes()`

| Variable | Type            | Usage   |
| -------- | --------------- | ------- |
| i        | `AtomicInteger` | counter |

```pseudocode
i = AomicInteger(1)
RETURN this.show(lambda p_index: str(i.get_and_increment()), this.horizontal_unit_side_length // 2, this.vertical_unit_side_length // 2)
```

#### `Board._show(symbolization, horizontal_margin, vertical_margin)`

| Variable          | Type       | Usage                                                    |
| ----------------- | ---------- | -------------------------------------------------------- |
| symbolization     | `Callable` | the function that converts piece indexes into characters |
| horizontal_margin | `int`      | horizontal margin one on each side                       |
| vertical_margin   | `int`      | vertical margin one at the top and one at the bottom     |
| s                 | `str`      | return string                                            |
| r                 | `str`      | block separator                                          |
| b                 | `str`      | blank line                                               |
| sp                | `str`      | line                                                     |

```pseudocode
s = r = (" " + this.horizontal_border * this.horizontal_unit_side_length) * this.width + linesep
FOR row OF this.p_map:
	b = ((this.vertical_border + " " * this.horizontal_unit_side_length) * this.width + this.vertical_border + linesep) * vertical_margin
	s += b
	p = ""
	FOR p_index OF row:
		sp += this.vertical_border + " " * horizontal_margin + (symbolization == null ? this.get_piece_symbol : symbolization)(p_index) * (this.horizontal_unit_side_length - 2 * horizontal_margin) + " " * horizontal_margin
		sp += this.vertical_border + _linesep
		s += sp * (this.vertical_unit_side_length - 2 * vertical_margin) + b + r
RETURN s
```

### `tictactoe/framework/player.py`

#### `Player.go(board)`

| Variable | Type    | Usage                 |
| -------- | ------- | --------------------- |
| board    | `Board` | the board             |
| d        | `list`  | the player's decision |

```pseudocode
decision = this.decide(COPY(board))
board.go(*d, this.p_index, false)
this.record_decisions.append(d)
```

#### `ProgramedPlayer.decide(board)`

| Variable | Type    | Usage     |
| -------- | ------- | --------- |
| board    | `Board` | the board |

```pseudocode
this.i++
RETURN this.i < this.decisions.length ? this.decisions[this.i] : this.player.decide(board)
```

#### `RandomPlayer.decide(board)`

| Variable | Type    | Usage             |
| -------- | ------- | ----------------- |
| board    | `Board` | the board         |
| choices  | `list`  | available choices |

```pseudocode
choices = board.blanks()
IF choices.length < 1 THEN RAISE GameOver
RETURN RANDOM_CHOICE(choices)
```

## TESTING

