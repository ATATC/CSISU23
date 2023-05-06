# Extension - Real AI

## Goal

The goal of this extension is to train a real deep-learning-based bot player.

## Design

### Neural Network Structure

<img src="./assets/nn_structure.jpg" alt="image-20230505135056969" style="zoom:50%;" />

The structure is very similar to my previous work [*A Deep Learning Model for Accurate and Robust Internet Traffic Classification*](https://github.com/ProjectNeura/A-Deep-Learning-Model-for-Accurate-and-Robust-Internet-Traffic-Classification). It takes in a 4-D tensor with the size of (`BATCH_SIZE`, 3, 3, 3). The other 2 channels are the previous piece map and the second previous piece map. The network outputs a distribution of probabilities indicating the scores of the 9 plaids plus a probability of afk, 10 elements in total.

### Training

`tictactoe.real_ai.boards.Boards` allows boards to be packed in batches. The model plays `BATCH_SIZE` games in parallel. Each game starts with the opponent going first, which is a `tictactoe.framework.RandomPlayer`. Every time the model gives an output, the loss is calculated using the Cross-Entropy method, comparing the output and `tictactoe.Bot`'s suggestion. The role of the rigid bot is very similar to a teacher in the distilling process. Then, instead of the model's output, the teacher's suggestion will be adopted to make the move.

Because the duration of every game is not constant, a hyperparameter `ROUND_LIMIT` is set to limit the number of rounds of each epoch. The boards are reset once they reach the `ROUND_LIMIT`. If a game ends before it reaches the limit, the teacher will give a suggestion for afk.

Calculated with simple math, it is not hard to realize that there are 9! which is 362880 different combinations for a board with the size of 3x3. Any `NUM_BATCHES` times `BATCH_SIZE` over 362880 should be sufficient.

In this particular experiment, the model only plays as the second player. When it plays as the first, the piece indexes on the board are inverted, meaning that 0 becomes 1 and 1 becomes 0. This makes a little sense to some extent, yet it is pretty much clear that it makes the model weaker when it plays as the first player.

One thing worth noticing while training is that the model is very sensitive to the choice of `ROUND_LIMIT`. A high `ROUND_LIMIT` can lead to excessive cases where the teacher teaches the model to afk and causes over-fitting, prematurely making the model surrender (referred to as afk above). In this case, another hyperparameter `ZERO_LIMIT` is introduced. Any harmful game after the limit is reached will be invalidated.

In the experiment, it seems that the higher the `ROUND_LIMIT` is the lower the `BATCH_SIZE` should be and `ROUND_LIMIT` should be less than 9.
$$
BS \le 8 \cdot 2^{9-RL}
$$

#### Specs of Trained Models / Evaluation

Each model is tested for 10k games. As there are random factors, the result might be slightly different every time.

**WP** shows two probabilities which are the chance that the model wins and the chance the opponent wins respectively.

**CD** shows the distribution of different conditions as `{someone won} / {tied} / {someone surrendered}`.

##### Playing as The First Player

| Model | WP   | CD   |
| ----- | ---- | ---- |
| 23m01 |      |      |
| 23m02 |      |      |
|       |      |      |

##### Playing as The Second Player

| Model | NUM_BATCHES | BATCH_SIZE | ROUND_LIMIT | ZERO_LIMIT | WP            | CD               |
| ----- | ----------- | ---------- | ----------- | ---------- | ------------- | ---------------- |
| 23m01 | 4000        | 32         | 7           | 0.1%       | 49.49% 26.96% | 7628 / 2355 / 17 |
| 23m02 | 4000        | 32         | 7           | 0          | 54.59% 24.00% | 7859 / 2400 / 0  |
| 23m03 | 4000        | 32         | 8           | 0          | 42.11% 28.72% | 7012 / 2917 / 71 |
| 23m04 | 4000        | 32         | 6           | 0          | 58.14% 23.25% | 8139 / 1861 / 0  |
| 23m05 | 4000        | 32         | 5           | 0          | 54.08% 25.98% | 7935 / 1994 / 71 |
| 23m06 | 4000        | 32         | 4           | 0          | 58.84% 20.58% | 7942 / 2058 / 0  |
| 23m07 | 4000        | 32         | 3           | 0          | 59.60% 21.22% | 8082 / 1918 / 0  |
| 23m08 | 8000        | 32         | 6           | 0          | 63.86% 19.90% | 8366 / 1624 / 10 |
| 23m09 | 8000        | 32         | 7           | 0          | 51.96% 24.58% | 7554 / 2446 / 0  |
| 23m10 | 8000        | 32         | 8           | 0          | 48.34% 26.00% | 7430 / 2566 / 4  |
| 23m11 | 8000        | 32         | 4           | 0          | 61.91% 21.35% | 8326 / 1674 / 0  |
| 23m12 | 8000        | 32         | 5           | 0          | 50.92% 25.07% | 7599 / 2401 / 0  |
| 23m13 | 40000       | 32         | 6           | 0          | 41.94% 29.34% | 7118 / 2872 / 10 |
| 23m14 | 40000       | 32         | 4           | 0          | 53.59% 25.58% | 7917 / 2083 / 0  |
| 23m15 | 40000       | 32         | 7           | 0          | 41.84% 30.46% | 7230 / 2770 / 0  |
| 23m16 | 40000       | 16         | 6           | 0          | 50.85% 25.10% | 7595 / 2405 / 0  |
| 23m17 | 40000       | 16         | 4           | 0          | 49.97% 27.77% | 7774 / 2226 / 0  |
| 23m18 | 8000        | 16         | 6           | 0          | 59.42% 23.63% | 8283 / 1695 / 22 |

## Testing

A variety of versions are trained with different hyperparameters. When testing the performance, they commonly show weakness in making appropriate decisions. Many of them even output invalid indexes or surrender prematurely.

### Showcase

The model sees the board differently in the following way:

```
 --------- --------- ---------
|         |         |         |
|    0    |    1    |    2    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|    3    |    4    |    5    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|    6    |    7    |    8    |
|         |         |         |
 --------- --------- ---------
```

#### Playing as The First

##### Case A

Model: `23m11`

```shell
AI output: 0.
 --------- --------- ---------
|         |         |         |
|    X    |         |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
```

```shell
AI output: 8.
 --------- --------- ---------
|         |         |         |
|    X    |         |    O    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |    X    |
|         |         |         |
 --------- --------- ---------
```

```shell
AI output: 6.
 --------- --------- ---------
|         |         |         |
|    X    |    O    |    O    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|    X    |         |    X    |
|         |         |         |
 --------- --------- ---------
```

```shell
AI output: 8.
WARNING: AI performed unexpectedly. Randomization intervened.
 --------- --------- ---------
|         |         |         |
|    X    |    O    |    O    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |    O    |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|    X    |    X    |    X    |
|         |         |         |
 --------- --------- ---------

AI A won!
```

In this game, we see that the model was trying to take corners. This is an effective strategy in Tic-Tac-Toe though, the model ignored the chances to attack. In the last step, the lack of the fourth step onwards in the training process causes the model to not make good judgments.

##### Case B

Model: `23m08`

```shell
AI output: 0.
 --------- --------- ---------
|         |         |         |
|    X    |         |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
```

```shell
AI output: 2.
 --------- --------- ---------
|         |         |         |
|    X    |         |    X    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |    O    |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|         |         |         |
|         |         |         |
 --------- --------- ---------
```

```shell
AI output: 3.
 --------- --------- ---------
|         |         |         |
|    X    |         |    X    |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|    X    |    O    |         |
|         |         |         |
 --------- --------- ---------
|         |         |         |
|    O    |         |         |
|         |         |         |
 --------- --------- ---------
```



#### Playing as The Second



## Limitations

Instead of training with reinforcement learning, it is somehow distilled from `tictactoe.Bot`. Due to the sketchy design, it does not show a state-of-art performance.

## Prospect

Reinforcement learning is very worth trying, yet it requires more effort to establish the loss function, so it is not included in this experiment as I have limited time to do the assignment.