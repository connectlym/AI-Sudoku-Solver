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

    def values_to_grid(self, values=None):
        """ Convert the dictionary board representation to as string.
        @:parameter
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
        #:return
            - grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        """

        if values is None:
            values = self.values

        res = []
        for r in self.rows:
            for c in self.cols:
                v = values[r + c]
                res.append(v if len(v) == 1 else '.')

        return ''.join(res)


    def grid_to_values(self, grid=None):
        """ Convert grid into a dict of {square: char}.
            Notice: '.' means empty.
        @:parameter
            - grid (str): string representing the sudoku grid
                  Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        @:return
            - values (dict): the dict storing all values (i.e. 'A1' => '135')
                            Empty values will be set to '.'
        """

        if grid is None:
            grid = self.grid

        sudoku_grid = {}
        for val, key in zip(grid, self.squares):
            if val == '.' or val == '0':
                sudoku_grid[key] = '.'
            else:
                sudoku_grid[key] = val

        return sudoku_grid

    ################ Games ################

    def remove_digit(self, square, digit):
        """ Remove a digit from the possible values of a box.
        @:parameter
            - square (str): the square to remove the digit from
            - digit (str): the digit to remove from the square
        @:return
            - values (dict): the dict values after updated
        """

        self.values[square] = self.values[square].replace(digit, '.')


    def display(self, values):
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


    def is_solved(self):
        """ Determine if the puzzle has been solved.
        @:return
            - solved (boolean): True if solved; False otherwise.
        """

        fully_reduced = all(len(self.values[s]) == 1 for s in self.squares)
        if not fully_reduced:
            return False

        for unit in self.unitlist:
            required_digits = '123456789'
            for box in unit:
                required_digits = required_digits.replace(self.values[box], '')
            if len(required_digits) != 0:
                return False

        return True