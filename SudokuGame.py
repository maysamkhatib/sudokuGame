import random
from abc import ABC, abstractmethod
import numpy as np


class Sudoku(ABC):
    # variable to count the points
    _points = 0

    # function to count the number of lines in the file (used in the load puzzle function)
    @staticmethod
    def numberOfLines(textFile, fileName):
        if textFile.closed:
            textFile = open(fileName, 'r')
        count = 0
        for _ in textFile:
            count += 1
        textFile.close()
        return count

    # function to load a puzzle from text file
    @staticmethod
    def loadPuzzle(textFile, fileName):
        # check if the number of rows is less than or equal 9 to continue
        if Sudoku.numberOfLines(textFile, fileName) > 9:
            raise Exception("Error: wrong rows number")
        # create 2d array to put the values in it
        puzzle1 = np.zeros((9, 9), dtype=int)
        # check if the file is closed to open it (the file should be opened)
        if textFile.closed:
            textFile = open(fileName, 'r')
        # the number of row that we will add the value in it
        row = 0
        for line in textFile:
            # to remove the new line
            line = line.split("\n")[0]
            # check if the number of columns is less than or equal 9 to continue
            if line.count(",") > 8:
                raise Exception("Error: wrong columns number")
            for i in range(0, line.count(",") + 1):
                value = line.split(",")[i]
                # if the value is a number from 0 to 9, then add it to the puzzle in its place
                if value.isdigit():
                    value = int(value)
                    if value > 9 or value < 1:
                        raise Exception("Error: invalid value in the puzzle!")
                    else:
                        puzzle1[row][i] = value
            row += 1
        # check if the puzzle is solvable, if it's not then exit the program
        tmp = np.copy(puzzle1)
        if Sudoku.solve(tmp):
            textFile.close()
            return puzzle1
        else:
            print("The puzzle from text file has no solution!!")
            exit(0)

    # function to check if the puzzle is solvable or not, and solve the puzzle if its solvable
    @staticmethod
    def solve(puzzle):
        # check if the puzzle is already solved (has no zeros in it)
        row = col = 0
        if 0 not in puzzle:
            return True
        else:
            # search for empty cells to fill it
            for i in range(81):
                row = int(i / 9)
                col = i % 9
                # exit the loop when find an empty cell
                if puzzle[row][col] == 0:
                    break
            # search for a suitable value to fill in the cell
            for i in range(1, 10):
                if Sudoku.checkIfValid(puzzle, row, col, i):
                    puzzle[row][col] = i
                    if Sudoku.solve(puzzle):
                        return True
                    # if the puzzle became not solvable after fill the previous value,
                    # then remove the value and search for another one
                    else:
                        puzzle[row][col] = 0
            # if the code reached here, that's mean the puzzle couldn't find a right solution for the puzzle
            return False

    # function to check if the value is valid in the specific cell
    @staticmethod
    def checkIfValid(puzzle, row, col, value):
        # if the number in the row, then it's invalid
        if value in puzzle[row]:
            return False
        # cif the number in the column, then it's invalid
        for i in range(9):
            if value == puzzle[i][col]:
                return False
        # check if the number in the box
        firstRowInBox = int(row / 3) * 3
        firstColInBox = int(col / 3) * 3
        for i in range(3):
            for j in range(3):
                # if the number in the box then it's invalid
                if puzzle[firstRowInBox + i][firstColInBox + j] == value:
                    return False
        # if the number is not in the same row or column or box, then the number is valid
        return True

    # this function is not certified because it has a big time complexity
    @staticmethod
    def randomly(level):
        puzzle = np.zeros((9, 9), dtype=int)
        noCells = 0
        if level == "E":
            noCells = int(9 * 9 * 0.4)
        elif level == "M":
            noCells = int(9 * 9 * 0.25)
        elif level == "D":
            noCells = int(9 * 9 * 0.1)

        # noCells = number of cells will be filled
        for i in range(noCells):
            # choose a random row, column, and a random value to put in the place
            value = random.randrange(1, 10)
            row = random.randrange(9)
            col = random.randrange(9)
            # if the specific cell has a value or the value is not valid then search again
            while puzzle[row][col] != 0 or not Sudoku.checkIfValid(puzzle, row, col, value):
                # choose a random row, column, and a random value to put in the place
                value = random.randrange(1, 10)
                row = random.randrange(9)
                col = random.randrange(9)
            else:
                puzzle[row][col] = value
        # check if the puzzle has a solution or not
        temp = np.copy(puzzle)
        if Sudoku.solve(temp):
            return puzzle
        else:
            Sudoku.randomly(level)

    # function to print the puzzle
    @staticmethod
    def printTable(puzzle):
        for i in range(9):
            if i % 3 == 0:
                print("\t\t\t-------------------------------------------------")
            print("\t\t\t", end="")
            for j in range(9):
                if j % 3 == 0:
                    print("|\t", end="")
                if puzzle[i][j] == 0:
                    print(f" \t", end="")
                else:
                    print(f"{puzzle[i][j]}\t", end="")
            print("|")
        print("\t\t\t-------------------------------------------------")

    # function to fill a cell in the puzzle
    def fill(self, puzzle):
        # check that the puzzle has empty cells
        if 0 not in puzzle:
            print("\t\t\tThe puzzle is already solved !")
            Sudoku.printTable(puzzle)
            return
        # try-except to deal with inputs error
        try:
            row = int(input("\t\t\tPlease enter the row number(from 1 to 9):\n\t\t\t>>>"))
            col = int(input("\t\t\tPlease enter the column number(from 1 to 9):\n\t\t\t>>>"))
            # check that the number in the range
            while row < 1 or row > 9 or col < 1 or col > 9:
                print("\t\t\tRow or column number is out of range !")
                row = int(input("\t\t\tPlease enter the row number(from 1 to 9):\n\t\t\t>>>"))
                col = int(input("\t\t\tPlease enter the column number(from 1 to 9):\n\t\t\t>>>"))
            else:
                value = int(input("\t\t\tPlease enter the value:\n\t\t\t>>>"))
                # if the cell is full, then ask the player to enter another value
                while puzzle[row - 1][col - 1] != 0:
                    Sudoku.printTable(puzzle)
                    print("\t\t\tThere's a value in this cell!!")
                    row = int(input("\t\t\tPlease enter the row number(from 1 to 9):\n\t\t\t>>>"))
                    col = int(input("\t\t\tPlease enter the column number(from 1 to 9):\n\t\t\t>>>"))
                    value = int(input("\t\t\tPlease enter the value:\n\t\t\t>>>"))
                else:
                    # put the values (row, column, the number) in the tuple
                    enteredValues = (row - 1, col - 1, value)
                    # copy the puzzle into a new puzzle and check if after adding the new value,
                    # the puzzle will still solvable.
                    newPuzzle = np.copy(puzzle)
                    newPuzzle[enteredValues[0]][enteredValues[1]] = enteredValues[2]
                    # if the new puzzle is solvable, then add the value to the original puzzle
                    # and add a point to the player
                    if Sudoku.solve(newPuzzle):
                        puzzle[enteredValues[0]][enteredValues[1]] = enteredValues[2]
                        self._points += 1
                        print("\t\t\t\t\t\t\t  Right Value :)")
                    # if it's not, deduct one point from the player
                    else:
                        self._points -= 1
                        print("\t\t\t\t\t\t\t  Wrong value!!")
                    Sudoku.printTable(puzzle)
        except:
            print("\t\t\tNon-integer value")

    @abstractmethod
    def hint(self, puzzle):
        pass

    # function to find an empty cell
    @staticmethod
    def findEmptyCell(puzzle):
        # return the first empty cell in the puzzle
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    return i, j
        return

    # generating a full puzzle board randomly
    @staticmethod
    def generateSolution(puzzle):
        numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row = col = 0
        for i in range(0, 81):
            row = int(i / 9)
            col = i % 9
            # find next empty cell
            if puzzle[row][col] == 0:
                random.shuffle(numberList)
                # pick a value from 0 to 9 randomly
                for number in numberList:
                    # if the picked number is valid then put it in the empty cell
                    if Sudoku.checkIfValid(puzzle, row, col, number):
                        puzzle[row][col] = number
                        if not Sudoku.findEmptyCell(puzzle):
                            return True
                        else:
                            # continue filling puzzle till it's filled
                            if Sudoku.generateSolution(puzzle):
                                # if the puzzle is full
                                return True
                break
        puzzle[row][col] = 0
        return False

    # function to remove numbers from the full puzzle to create a game in many levels
    @staticmethod
    def removeNumbersFromPuzzle(puzzle, level):
        # number of cells will be removed
        noCells = int(9 * 9 * level)
        for i in range(0, noCells):
            # choose a random row and a random column
            row = random.randrange(0, 9)
            col = random.randrange(0, 9)
            # if the specific cell is empty then search again
            while puzzle[row][col] == 0:
                # choose a random row, column to remove a value from them
                row = random.randrange(0, 9)
                col = random.randrange(0, 9)
            else:
                # if the cell have a value then remove it
                puzzle[row][col] = 0
        return puzzle

    # function to find a random puzzle has a solution
    @staticmethod
    def random(level):
        # the puzzle we will fill it
        puzzle = np.zeros((9, 9), dtype=int)
        # generate a full solution for a puzzle
        Sudoku.generateSolution(puzzle)
        if level == "E":
            # remove 60% of cells in the puzzle
            Sudoku.removeNumbersFromPuzzle(puzzle, 0.6)
        elif level == "M":
            # remove 75% of cells in the puzzle
            Sudoku.removeNumbersFromPuzzle(puzzle, 0.75)
        elif level == "D":
            # remove 90% of cells in the puzzle
            Sudoku.removeNumbersFromPuzzle(puzzle, 0.9)
        return puzzle

    # function to return the number of points
    def getPoints(self):
        return self._points

    # function to set a value to the points
    def setPoints(self, points):
        self._points = points

    @abstractmethod
    def calculateScores(self, timeForPlayer, timeForAnotherPlayer=None):
        pass
