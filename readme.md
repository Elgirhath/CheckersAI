# CheckersAI

Fully working checkers game with support for playing:
* player vs player
* player vs computer
* computer vs computer

Here is the sample gameplay of computer vs computer:

![Demo CountPages alpha](clip.gif)

To run the game call:

``` powershell
python main.py -pc
```

You will need tensorflow and numpy. The flag `-pc` runs a game for player (white) vs computer (black). Available flags:

``` powershell
-pp #player vs player
-pc #player (white) vs computer (black)
-cp #computer (white) vs player (black)
-cc #computer vs computer
```

## How it's done

The AI is based on a neural network which evaluates board states. This neural network is taught on the dataset of games played by computer vs computer, where each record represents a state of the game and its output.

A search tree is used to evaluate future positions. The above gif represents a game in which search tree of depth 4 was used. Each layer of nodes creates a huge amount of new positions to evaluate and I used Alpha-Beta pruning to reduce it.

## Tests

The file `tests/tests.py` includes sample e2e tests which check if the computer plays the best moves in given situations even when it means sacrificing a queen.

Run the tests with:

``` powershell
python run_tests.py --debug # where --debug is optional and displays visual representation of the tests
```