# ------------------------------
#       Solver for sudoku.
# ------------------------------
# Original contributor: Peter Norvig
# Modified by YM Li, in Spring 2018,
# at Union College, NY, US,
# for the final project of CSC320 - Artificial Intelligence.
# ------------------------------
# References:
# 1. Solving Every Sudoku Puzzle, Peter Norvig,
#   http://www.norvig.com/sudoku.html
# 2. Solving Every Sudoku Puzzle (code), Peter Norvig,
#   https://gist.github.com/neilalbrock/894520
# 3. Sudoku Solver | AI Agent, Prakhar Mishra,
#   https://medium.com/@pmprakhargenius/sudoku-solver-ai-agent-700897b936c7
# 4. Sudoku Tutorial 2 - Naked Pairs, dkmgames
#   https://www.youtube.com/watch?v=KUF_P9LypNs

from game import Sudoku


class Solver():
    """Class that solves sudoku games."""

    rows = 'ABCDEFGHI'
    cols = '123456789'

    def __init__(self, puzzle):
        """ Initialize the puzzle.
        @:parameter:
            - puzzle (Sudoku obj): the instance of a Sudoku we are trying to solve
        """

        self.squares = puzzle.squares
        self.unitlist = puzzle.unitlist
        self.units = puzzle.units
        self.peers = puzzle.peers


    def assign(self, values, s, d):
        """ Eliminate all the other values (except d) from values[s] and propagate.
        @:parameter
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
            - s (key): the selected square
            - d (int): the selected value
        @:return
            - values (dict), or False if a contradiction is detected.
        """

        other_values = values[s].replace(d, '')

        # if all(self.eliminate(values, s, d2) for d2 in other_values):
        #     return values
        # else:
        #     return False
        for i in other_values:
            if self.eliminate(values, s, i) == False:
                return False

        return values


    def eliminate(self, values, s, d):
        """Eliminate d from values[s]; propagate when values or places <= 2.
        @:parameter
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
            - s (key): the selected square
            - d (int): the selected value
        @:return
            - values (dict), or False if a contradiction is detected.
        """

        if d not in values[s]:
            return values  ## Already eliminated

        values[s] = values[s].replace(d, '')

        ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values[s]) == 0:
            return False  ## Contradiction: removed last value
        elif len(values[s]) == 1:
            d2 = values[s]
            if not all(self.eliminate(values, s2, d2) for s2 in self.peers[s]):
                return False

        ## (2) If a unit u is reduced to only one place for a value d, then put it there.
        for u in self.units[s]:
            dplaces = [s for s in u if d in values[s]]
            if len(dplaces) == 0:
                return False  ## Contradiction: no place for this value
            elif len(dplaces) == 1:
                # d can only be in one place in unit; assign it there
                if not self.assign(values, dplaces[0], d):
                    return False

        return values


    def search(self, values):
        """Using DFS and propagation, try all possible values.
        @:parameter
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
        @:return
            - values (dict) if solved, False if cannot be solved.
        """

        if values is False:
            return False  ## Failed earlier

        if all(len(values[s]) == 1 for s in self.squares):
            return values  ## Solved!

        ## Chose the unfilled square s with the fewest possibilities
        n, s = min((len(values[s]), s) for s in self.squares if len(values[s]) > 1)

        return self.some(self.search(self.assign(values.copy(), s, d))
                    for d in values[s])


    def some(self, seq):
        "Return some element of seq that is true."
        for e in seq:
            if e: return e
        return False


    def solve(self, grid):
        return self.search(Sudoku.grid_to_values(grid))
