<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/UPocek/Othello/blob/main/results/ai.png">
    <img alt="Flutter" src="https://github.com/UPocek/Othello/blob/main/results/ai.png">
  </picture>
</h1>

# Othello
AI that plays the game Othello/Reversi against you.

## More pieces of information

### Idea

This was my student assignment in the first year of college on the subject called "Algorithms and data structures" by professor Branko Milosavljevic.

### Implementation

As at that time console applications were the only thing I knew how to make, so it doesn't have a cool GUI but steel is pretty fun to play.

It uses [minimax](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/) algorithm with [alfa-beta pruning](https://www.mygreatlearning.com/blog/alpha-beta-pruning-in-ai/) to find the best move possible. Also because I optimized board storing and heuristic calculation for every position I was able to make it predict up to 7 turns in advanced so good luck trying to beat it.

Regarding the structures used to design the project, I implemented my version of ChainedHashMap to store already calculated board positions (as one of the optimization techniques) and also I implemented BinaryTree used for pruning. Since it was one of the requirements of the project all the calculations are done in less than 3 seconds so you feel like you are playing against a real pro.

### Recources used

- https://www.eothello.com/
- https://www.ultraboardgames.com/othello/tips.php
- https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
- https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
- https://www.hindawi.com/journals/mpe/2015/637809/
