# ------------------------------
#       A 9x9 Sudoku Game.
# ------------------------------
# Original contributor: Zack Thoutt
# Original version: https://github.com/zackthoutt/sudoku-ai
# Modified by YM Li, Caleb Seymour, in Spring 2018,
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

class Sudoku():
    """The sudoku game."""

    ## Throughout this program we have:
    ##   r is a row,    e.g. 'A'
    ##   c is a column, e.g. '3'
    ##   s is a square, e.g. 'A3'
    ##   d is a digit,  e.g. '9'
    ##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
    ##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
    ##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
    ##      i.e.
    ##      A1 A2 A3| A4 A5 A6| A7 A8 A9
    ##      B1 B2 B3| B4 B5 B6| B7 B8 B9
    ##      C1 C2 C3| C4 C5 C6| C7 C8 C9
    ##      ---------+---------+---------
    ##      D1 D2 D3| D4 D5 D6| D7 D8 D9
    ##      E1 E2 E3| E4 E5 E6| E7 E8 E9
    ##      F1 F2 F3| F4 F5 F6| F7 F8 F9
    ##      ---------+---------+---------
    ##      G1 G2 G3| G4 G5 G6| G7 G8 G9
    ##      H1 H2 H3| H4 H5 H6| H7 H8 H9
    ##      I1 I2 I3| I4 I5 I6| I7 I8 I9

    rows = "ABCDEFGHI"
    cols = "123456789"

    ################ Initialization ################

    def __init__(self, iniGrid):
        """ Initialize the Sudoku puzzle.
        @:parameter
            - iniGrid (str): a string representing the sudoku grid.
                i.e. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        """

        # Check if the initialization arg is 81-char-long or not.
        if len(iniGrid) != 81:
            raise Exception("Initialization Error - Grid must be 81 characters.")

        self.build_game() # build the game
        self.iniGrid = iniGrid
        self.grid = iniGrid
        self.values = self.grid_to_values(iniGrid)


    def build_game(self):
        """ Build the game of sudoku puzzle."""

        # self.squares = [r + c for r in self.rows for c in self.cols]
        self.squares = self.cross(self.rows, self.cols)

        # unitlist = ([cross(rows, c) for c in cols] +
        #            [cross(r, cols) for r in rows] +
        #            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

        self.columnUnits = [self.cross(self.rows, c) for c in self.cols]
        self.rowUnits = [self.cross(r, self.cols) for r in self.rows]
        self.squareUnits = [self.cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        self.unitlist = self.columnUnits + self.rowUnits + self.squareUnits

        # units = dict((s, [u for u in unitlist if s in u])
        #             for s in squares)

        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)

        # peers = dict((s, set(sum(units[s], [])) - set([s]))
        #             for s in squares)

        self.peers = dict( (s, set( sum(self.units[s],[]) ) - set([s]) ) for s in self.squares)


    @staticmethod
    def cross(A, B):
        """Cross product of elements in A and elements in B """
        return [a+b for a in A for b in B]

    ################ Unit Tests ################

    def test(self):
        "A set of tests that must pass."

        assert len(self.squares) == 81
        assert len(self.unitlist) == 27
        assert all(len(self.units[s]) == 3 for s in self.squares)
        assert all(len(self.peers[s]) == 20 for s in self.squares)

        assert self.units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                               ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                               ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]

        assert self.peers['C2'] == {['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                                   'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                                   'A1', 'A3', 'B1', 'B3']}

        print('All tests pass.')

    ################ Grids ################

    def values_to_grid(self, values):
        """ Convert the dictionary board representation to as string.
        @:parameter
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
        #:return
            - grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        """
        digits = '123456789'
        chars = [c for c in self.grid if c in digits or c in '0.']

        assert len(chars) == 81

        return dict(zip(self.squares, chars))


    def grid_to_values(self, grid):
        """ Convert grid into a dict of {square: char}.
            Notice: '.' means empty.
        @:parameter
            - grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        @:return
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
                            Empty values will be set to '.'
        """

        ## To start, every square can be any digit; then assign values from the grid.
        digits = '123456789'
        values = dict((s, digits) for s in self.squares)

        for s, d in self.values_to_grid(grid).items():
            if d in digits and not self.assign(values, s, d):
                return False  ## (Fail if we can't assign d to square s.)

        return values

    ################ Games ################

    def displaySolver(self):
        """ Display the values as a 2-D grid.
        @:parameter
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
        """

        width = 1+max(len(self.values[s]) for s in self.squares)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(self.values[r+c].center(width)+('|' if c in '36' else '')
                          for c in self.cols))
            if r in 'CF': print(line)
        print()

    ################ Solver ################

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
            if e:
                return e
        return False


    def solve(self, grid):
        return self.search(Sudoku.grid_to_values(self, grid))

