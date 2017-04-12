# N-Size Tic-Tac-Toe

Play tic-tac-toe against the computer in any size grid.

## Running

```
./tictactoe.py
```

It will prompt you the grid size (square grids only), whether you want X or O (X goes first), and the AI module (press ENTER for random).


## AI Modules

### random

Simply picks a random square each time. Easy to beat.

### block_and_score

Similar to how humans play tic tac toe, although it does not plan ahead. If it sees that it has 1 square left to win, it will go there. If it sees that the player has 1 square left to win, it will block that win. Otherwise fall back to random.
 
