import random
from abc import ABC

import numpy as np

import OnePlayerMode as OM
import SudokuGame as game


class TwoPlayersMode(OM.OnePlayerMode, game.Sudoku, ABC):
    # constructor method
    def __init__(self):
        super().__init__()
        self._points = 0

    def hint(self, puzzle):
        # check that the puzzle has empty cells
        if 0 not in puzzle:
            print("\t\t\tThe puzzle is already solved !")
            game.Sudoku.printTable(puzzle)
            return
        # solve a puzzle and save it in another puzzle (temp)
        temp = np.copy(puzzle)
        game.Sudoku.solve(temp)
        # pick a random cell to put the hint in it
        selectedRow = random.randrange(0, 9)
        selectedCol = random.randrange(0, 9)
        # if the random cell has a value, then search for another one
        while puzzle[selectedRow][selectedCol] != 0:
            selectedRow = random.randrange(0, 9)
            selectedCol = random.randrange(0, 9)
        else:
            # save the hint value in a "value" variable
            value = temp[selectedRow][selectedCol]
            hint = (selectedRow, selectedCol, value)
            # put the hint in the puzzle
            puzzle[hint[0]][hint[1]] = hint[2]
        print(f"\t\t\tThe value in row {hint[0] + 1} and column {hint[1] + 1} is: "
              f"{hint[2]}")
        game.Sudoku.printTable(puzzle)

    # function to calculate the scores of the player
    def calculateScores(self, timeForPlayer, timeForAnotherPlayer=None):
        if timeForAnotherPlayer is None:
            raise Exception("Missing attribute !")
        if self._points <= 0:
            return 0
        else:
            scores = (self._points / 81) * ((timeForPlayer + timeForAnotherPlayer) / timeForPlayer)
            return scores
