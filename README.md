# CSISU23
ICS3U Assignment at Villanova College

## Usage

### Run

```shell
python3 tictactoe/main.py
```

### Enable Real AI

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

Notice that the model file must exist as `.model/23m05.pth`. Make sure you set the working directory to the root of the project.
