import game

def main():
    dokesStr = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    dokes = game.Sudoku(dokesStr)
    dokes.display(dokesStr)
    #dokes.test()

if __name__ == "__main__":
    main()
