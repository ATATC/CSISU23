# CSISU23

ICS3U Assignment at Villanova College

## Features

- A universal board framework with high extensibility
- Scalable rendering
- Score counter
- Input error detection
- A robust bot
- Optional real AI (not if-else)
- ***Extremely standardized code formatting***

## Assignment Document

See *CSISU23.md*.

## Usage

### Run

Make sure you set the working directory to the root of the project.

```shell
python3 main.py
```

### Train

Make sure you set the working directory to the root of the project.

```shell
python3 train.py
```

The script does not support CUDA acceleration for now.

### Real AI

#### Enable Real AI

You will have to install [PyTorch](https://pytorch.org) and edit `main.py`.

1. Locate the following lines

   ```python
   player_a, rd_dir_a = choose_player("A", 0)
   player_b, rd_dir_b = choose_player("B", 1)
   ```

2. Change the lines above to the following

   ```python
   player_a, rd_dir_a = choose_player("A", 0, ai_bot=True)
   player_b, rd_dir_b = choose_player("B", 1, ai_bot=True)
   ```

3. Locate the following lines

   ```python
   (player_a if board.get_round_counter() % 2 == 0 else player_b).go(board)
   print(board)
   ```

4. Insert the following code after the first line

   ```python
   if type(player_a) != HumanPlayer:
       player_a.step(board)
   if type(player_b) != HumanPlayer:
       player_b.step(board)
   ```

   It should look like this finally:

   ```python
   (player_a if board.get_round_counter() % 2 == 0 else player_b).go(board)
   if type(player_a) != HumanPlayer:
       player_a.step(board)
   if type(player_b) != HumanPlayer:
       player_b.step(board)
   print(board)
   ```

5. Append the following code to the end of the file

   ```python
   if type(player_a) != HumanPlayer:
       player_a.clear()
   if type(player_b) != HumanPlayer:
       player_b.clear()
   ```

   Make sure it is under the `while True` loop.

Notice that the model file must exist as `.model/23mxx.pth`. You will find trained models under the folder `model`.
Rename the model you pick to `23mxx.pth` so that the program can find it successfully.

For more information see *Extension - Real AI.md*.

