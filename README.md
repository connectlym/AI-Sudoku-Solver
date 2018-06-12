# AI-Sudoku-Solver

## Purposes

This is the final project of the course CSC 320 Artificial Intelligence at Union College in Spring 2018.
The main purpose of this project is to understand the ways to implement an agent to solve sudoku puzzles.


To test the result, see file sudoku_client.py.


## Getting Started

A Sudoku puzzle is a grid of 81 squares; the majority of enthusiasts label the columns 1-9, the rows A-I, and call a
collection of nine squares (column, row, or box) a unit and the squares that share a unit the peers. A puzzle leaves
some squares blank and fills others with digits, and the whole idea is that a puzzle is solved if the squares in each
unit are filled with a permutation of the digits 1 to 9. That is, no digit can appear twice in a unit, and every digit
must appear once. This implies that each square must have a different value from any of its peers.


Those with experience solving Sudoku puzzles know that there are two important strategies that we can use to make
progress towards filling in all the squares:

(1) If a square has only one possible value, then eliminate that value from the square's peers.

(2) If a unit has only one possible place for a value, then put the value there.


But these basic rules are not useful when doing tough puzzles. So, we need to improve our solutions. A better solution
is called Naked Twins Rule, which is useful when there exists a twin of numbers in same column or row or square. But it
is still not working for some puzzles.


Thus, we improve again and now have a better solution which use DFS search with backtracking to search for the solution
of each blank.


### Prerequisites

Python 3


## Contributors

* [YM Li](https://github.com/MonicaLiii)
* [Caleb Seymour](https://github.com/ccmour)
* [Luke Yu](https://github.com/zyu15)

## Acknowledgments

* [Solving Every Sudoku Puzzle, Peter Norvig](http://www.norvig.com/sudoku.html)
* [Solving Every Sudoku Puzzle (code), Peter Norvig](https://gist.github.com/neilalbrock/894520)
* [Sudoku Solver | AI Agent, Prakhar Mishra](https://medium.com/@pmprakhargenius/sudoku-solver-ai-agent-700897b936c7)
* [Sudoku Tutorial 2 - Naked Pairs, dkmgames](https://www.youtube.com/watch?v=KUF_P9LypNs)
* [Sudoku Dragon](http://www.sudokudragon.com/tutorialnakedtwins.htm)