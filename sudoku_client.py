# ------------------------------
#       Client for sudoku.
# ------------------------------
# By Caleb Seymour, in Spring 2018,
# at Union College, NY, US,
# for the final project of CSC320 - Artificial Intelligence.
# ------------------------------

import game

def main():
    grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    game1 = game.Sudoku(grid1)
    game1.displaySolver()

    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    game2 = game.Sudoku(grid2)
    game2.displaySolver()
    #game2.test()
    solved2 = game2.solve(grid2)
    print(solved2)
    ## Problem left here: Cannot printout the correct soln, although it has been solved (see the printed dict).
    solved2 = game2.solveNakedTwins(grid2)
    print(solved2)


if __name__ == "__main__":
    main()
