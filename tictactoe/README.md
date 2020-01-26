## Tic-Tac-Toe-Engine
### Quickstart
To play a quick round of Tictactoe against the AI, go to the `tictactoe` directory and run `python demo.py`

The code is written in python 3.7 and does only need the math and random modules.
### Tech
#### Approach
Tic-Tac-Toe is a deterministic game with no hidden information, where players take turns. Each game state is either a win-state, a lose-state or a draw-state.

The total state space is rather small (a simple upper bound is 9!=362880, the true number of possible games is much smaller), so we can traverse the full state space and mark each state as either win, lose or draw.

The AI implements an exhaustive tree-search. Intermediate results are cached. By this approach, the AI does not use any Tictactoe-specific knowledge except for the game rules (Similarly to AlphaZero that can play a variety of games, while the older AlphaGo used Go-specific knowledge).

Thanks to the generic implementation, the AI can play other games as well, as long as they are deterministic, have no hidden information and are reasonably small.

#### Implementation
I went for a modular implementation: Players can be exchanges (human player, AI player, random player) and the game itself can be replaced by other games.

A `Session` object manages the games. It is initialized with a game object (containing the game rules) and two player objects. Games and players are implemented in the games and players submodules.

```python
import game_ai as ga
game = ga.games.Tictactoe
player1 = ga.players.HumanPlayer()
player2 = ga.players.AIPlayer()
s = ga.Session(ga.games.Tictactoe, player1, player2)
```

You can now start a match:
```python
s.play()
```

The actual AI code lies in the class `AIPlayer` in `players.py`.

Some terminology:

A __position__ is a gamestate (Where are the X's and O's?)

A __game__ is similar to a rulebook. It contains information about the starting position of the game, rules  defining what moves are possible in each situation, rules defining the end of the game and who won. For user interaction it also contains written instructions and a function for displaying the game's position on screen.

A __table__ (like in dinner table) manages gamestates during a match (=a game that is played) It keeps track of the changing position and makes sure all moves are legal. It contains a _position_ and a _game_. Imagine sitting at the table with some friends. On the table, there is the game board with all the pieces (=the position) and the rulebook (=the game)

A __player__ is an object that can make moves. It needs to access the table, so it can see the position and the game rules. The two players `AIPlayer` and `RandomPlayer` select moves algorithmically, while `HumanPlayer` asks the user to input moves.

A __session__ can be thought of as a referee or game master. It starts with a _game_ and two _players_. Then it sets up a new table and makes sure the two players take their turn. After each move, it checks if someone has won the game.

### Possible Extensions
#### Larger state spaces
The given AI will in theory work for games like chess and go, but not in practice, due to the huge state spaces.
Some ideas for approaching bigger games:

  1. Many positions are symmetric. Exploiting symmetry will reduce the size of the game tree without introducing errors. For chess and go, this will not be enough, though.
  2. Limit the tree search to a specific depth and then use a heuristic to evaluate position.
  3. Use MCTS (Monte Carlo Tree Search). This method does not traverse the full game tree but instead samples random trajectories.

Numbers 2. and 3. will not result in perfect play, but only in approximately-perfect play.

#### Other game types
__Games with randomness__ (backgammon,...) can theoretically be approach with the same tree-search idea. The main difference is that positions are no longer discrete (win/loss/draw) but instead have a win-percentage.

__Games with simultaneous turn__ this type of game is treated in game theory and uses very different approaches.

__Games with hidden information__ ->game theory as well.