# CSISU23
ICS3U Assignment at Villanova College

## Usage

### Run

```shell
python3 src/main.py
```

### Enable Real AI

You will have to install [PyTorch](https://pytorch.org) and edit `src/tictactoe.py`.

Add this line to the top:

```python
from real_ai import load_from
```

Then locate the following line in the function `choose_player()`:

```python
player = Bot(f"Bot {serial}", p_index)
```

Change the line above to the following:

```python
player = load_from("./m/20230504B0.pth", name=f"AI {serial}", p_index=p_index)
```

