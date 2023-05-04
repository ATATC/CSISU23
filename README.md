# CSISU23

ICS3U Assignment at Villanova College

## Features

- A universal board framework with high extensibility
- Scalable rendering
- Input error detection
- A robust bot
- Optional real AI (not if-else)
- ***Extremely standardized code formatting***

## Usage

### Run

```shell
python3 main.py
```

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

Notice that the model file must exist as `.model/23m05.pth`. Make sure you set the working directory to the root of the project.

#### Limitations

The structure is very similar to LeNet-5. It takes in a 4-D tensor with the size of (batch_size, 3, 3, 3). The other 2 channels are the previous piece map and the second previous piece map. The network outputs a distribution of probabilities indicating the scores of the 9 plaids.

Instead of training with reinforcement learning, it is somehow distilled from `tictactoe.Bot`. Due to the sketchy design, it does not show a state-of-art performance.

**It seems that the higher the `ROUND_LIMIT` is the lower the `BATCH_SIZE` should be and `ROUND_LIMIT` should be less than 9.** 
$$
BS \le 8 \cdot 2^{9-RL}
$$

#### Prospect

Reinforcement learning is very worth trying, yet it requires more effort to establish the loss function, so it is not included in this experiment as I have limited time to do the assignment.
