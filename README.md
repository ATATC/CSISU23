# CSISU23

ICS3U Assignment at Villanova College

## Usage

### Run

```shell
python3 main.py
```

### Real AI

#### Enable Real AI

You will have to install [PyTorch](https://pytorch.org) and edit `main.py`.

Locate the following lines:

```python
player_a, rd_dir_a = choose_player("A", 0)
player_b, rd_dir_b = choose_player("B", 1)
```

Change the lines above to the following:

```python
player_a, rd_dir_a = choose_player("A", 0, ai_bot=True)
player_b, rd_dir_b = choose_player("B", 1, ai_bot=True)
```

Notice that the model file must exist as `.model/23m05.pth`. Make sure you set the working directory to the root of the
project.

#### Limitations

The structure is very similar to LeNet-5. It takes in a 4-D tensor with the size of (batch_size, 3, 3, 3). 
The other 2 channels are the previous piece map and the second previous piece map multiply weights of 0.5 and 0.25 respectively. 
Instead of trained with Reinforcement Learning, it is somehow distilled from `tictactoe.Bot`. Due to the sketchy design, it does not show a state-of-art performance.
