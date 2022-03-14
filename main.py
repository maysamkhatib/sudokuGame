import numpy as np
import SudokuGame
import OnePlayerMode as OM
import TwoPlayersMode as TM
from time import time


if __name__ == '__main__':
    # ask user to choose an option (load a puzzle or start a random one)
    print("\t-----------------------------------------------------")
    print("\t-----------------------------------------------------")
    print("\t\t\tHello, please choose an option:")
    print("\t\t\t1- load a puzzle from a text file")
    print("\t\t\t2- start a random puzzle")
    option = input("\t\t\t>>>")
    # declare the puzzle we will use in the whole game
    puzzle = np.zeros((9, 9), dtype=int)
    while True:
        # ############################################################################################################ #
        # ---------------------------------------------LOAD PUZZLE---------------------------------------------------- #
        # ############################################################################################################ #
        if option == '1':
            try:
                fileName = "sudokufile.txt"
                file = open(fileName, 'r')
            except IOError:
                # raise an error if the file is not exist
                raise Exception("Error: The file is not exist")
            else:
                # get mode from the user
                mode = input(
                    "\t\t\tPlease choose the mode:\n\t\t\t1-One player mode\n\t\t\t2-Two players mode\n\t\t\t>>>")
                # if the input mode is an invalid value, then ask the user to input the valid value !
                while mode != "1" and mode != "2":
                    print("\t\t\tInvalid value!")
                    mode = input(
                        "\t\t\tPlease choose the mode:\n\t\t\t1-One player mode\n\t\t\t2-Two players mode\n\t\t\t>>>")
                # ---------------------------------------------------------------------------------------------------- #
                # ----------------------------------------ONE PLAYER MODE--------------------------------------------- #
                # ---------------------------------------------------------------------------------------------------- #
                if mode == "1":
                    player = OM.OnePlayerMode()
                    puzzle = player.loadPuzzle(file, fileName)
                    # save the starting time to use it in the total score
                    startingTime = time()
                    player.printTable(puzzle)
                    # ask the player to choose a game option (fill, hint, or solve)
                    print("\t\t\tChoose an option:")
                    print("\t\t\tF: Fill\n\t\t\tH: Hint (you will lose 2 points)\n\t\t\tS: Solve")
                    gameOption = input("\t\t\t>>>")
                    # if the option is "S" the game will end
                    while gameOption != "S":
                        # if the puzzle is solved, the game will end
                        checkIfSolved = 0 not in puzzle
                        if checkIfSolved:
                            print("\t\t\tThe puzzle is already solved!")
                            break
                        # if the option is "F" then the player will fill one cell, if the value is right,
                        # then the player will gain 1 point. If it's not, then he will lose 1 point
                        if gameOption == "F":
                            player.fill(puzzle)
                        # if the option is "H" then one cell will be solved, and the player will lose 2 points
                        elif gameOption == "H":
                            player.hint(puzzle)
                        else:
                            print("\t\t\tInvalid value!!")
                        print("\t\t\tChoose an option:")
                        print("\t\t\tF: Fill\n\t\t\tH: Hint (you will lose 2 points)\n\t\t\tS: Solve")
                        gameOption = input("\t\t\t>>>")
                    # the total time is equal the end time - starting time
                    totalTime = time() - startingTime
                    # calculate the scores after ending the game
                    scores = player.calculateScores(totalTime)
                    print("\t\t\tYour total score is: ", scores)
                    player.solve(puzzle)
                    player.printTable(puzzle)
                # ---------------------------------------------------------------------------------------------------- #
                # ----------------------------------------TWO PLAYERS MODE-------------------------------------------- #
                # ---------------------------------------------------------------------------------------------------- #
                else:
                    playerNumber = 0
                    player1 = TM.TwoPlayersMode()
                    player2 = TM.TwoPlayersMode()
                    puzzle = SudokuGame.Sudoku.loadPuzzle(file, fileName)
                    # these variables to save the total time for each player
                    totalTime1 = totalTime2 = 0
                    startingTime = time()
                    SudokuGame.Sudoku.printTable(puzzle)
                    # ask the player to choose a game option (fill, pass, or solve)
                    print(f"\t\t\tPlayer{playerNumber+1} turn")
                    print("\t\t\tChoose an option:")
                    print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                    gameOption = input("\t\t\t>>>")
                    noPass = 0
                    # if the option is "S" the game will end
                    while gameOption != "S":
                        # if the puzzle is solved, the game will end
                        checkIfSolved = 0 not in puzzle
                        if checkIfSolved:
                            print("\t\t\tThe puzzle is already solved!")
                            break
                        # ---------------------------------------Player1---------------------------------------------- #
                        if playerNumber == 0:
                            # if the option is "F" then the player will fill one cell, if the value is right,
                            # then the player will gain 1 point. If it's not, then he will lose 1 point
                            if gameOption == "F":
                                player1.fill(puzzle)
                                # reset noPass (we have to check if the four passes are sequentially)
                                noPass = 0
                            # if the option is "P" then the turn will be for the other player
                            elif gameOption == "P":
                                noPass += 1
                                player1.setPoints((player1.getPoints() - 1))
                                # after four passes (in sequence) the game will display a hint
                                if noPass == 4:
                                    noPass = 0
                                    print("\t\t\t\t\t HINT:")
                                    player1.hint(puzzle)
                                else:
                                    player1.printTable(puzzle)
                            else:
                                print("\t\t\tInvalid option!!")
                                print(f"\t\t\tPlayer{playerNumber+1} turn")
                                print("\t\t\tChoose an option:")
                                print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                                gameOption = input("\t\t\t>>>")
                                continue
                            # after finishing the player's turn,
                            # the time was spend in this turn will be added to the total time
                            totalTime1 += time() - startingTime
                            # the starting time for the other player
                            startingTime = time()
                        # ---------------------------------------Player2---------------------------------------------- #
                        elif playerNumber == 1:
                            # if the option is "F" then the player will fill one cell, if the value is right,
                            # then the player will gain 1 point. If it's not, then he will lose 1 point
                            if gameOption == "F":
                                player2.fill(puzzle)
                                # reset noPass (we have to check if the four passes are sequentially)
                                noPass = 0
                            # if the option is "P" then the turn will be for the other player
                            elif gameOption == "P":
                                noPass += 1
                                player2.setPoints(player2.getPoints() - 1)
                                # after four passes (in sequence) the game will display a hint
                                if noPass == 4:
                                    noPass = 0
                                    print("\t\t\tHINT:")
                                    player2.hint(puzzle)
                                else:
                                    player2.printTable(puzzle)
                            else:
                                print("\t\t\tInvalid option!!")
                                print(f"\t\t\tPlayer{playerNumber+1} turn")
                                print("\t\t\tChoose an option:")
                                print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                                gameOption = input("\t\t\t>>>")
                                continue
                            # after finishing the player's turn,
                            # the time was spend in this turn will be added to the total time
                            totalTime2 += time() - startingTime
                            startingTime = time()
                        # the roles are switched between players
                        playerNumber = (playerNumber + 1) % 2
                        print(f"\t\t\tPlayer{playerNumber+1} turn")
                        print("\t\t\tChoose an option:")
                        print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                        gameOption = input("\t\t\t>>>")
                    # after ending the game, the player who ended the game,
                    # the time will be added to the total time of him
                    if playerNumber == 0:
                        totalTime1 += time() - startingTime
                        startingTime = time()
                    else:
                        totalTime2 += time() - startingTime
                        startingTime = time()
                    # at the end of the game, the scores will be calculated
                    scores1 = player1.calculateScores(totalTime1, totalTime2)
                    scores2 = player2.calculateScores(totalTime2, totalTime1)
                    print("\t\t\tThe player1 total score is:", scores1)
                    print("\t\t\tThe player2 total score is:", scores2)
                    SudokuGame.Sudoku.solve(puzzle)
                    SudokuGame.Sudoku.printTable(puzzle)
            break
        # ############################################################################################################ #
        # -------------------------------------------RANDOM PUZZLE---------------------------------------------------- #
        # ############################################################################################################ #
        elif option == '2':
            # ask the player to choose the level difficulty
            print("\t\t\tPlease choose the level:")
            print("\t\t\tE: Easy (40% of cells automatically filled)")
            print("\t\t\tM: Medium (25% of cells automatically filled)")
            print("\t\t\tD: Difficult (10% of cells automatically filled)")
            level = input("\t\t\t>>>")
            while level != "E" and level != "M" and level != "D":
                print("\t\t\tInvalid value!")
                print("\t\t\tE: Easy (40% of cells automatically filled)")
                print("\t\t\tM: Medium (25% of cells automatically filled)")
                print("\t\t\tD: Difficult (10% of cells automatically filled)")
                level = input("\t\t\t>>>")
            else:
                # get mode from the user
                mode = input(
                    "\t\t\tPlease choose the mode:\n\t\t\t1-One player mode\n\t\t\t2-Two players mode\n\t\t\t>>>")
                while mode != "1" and mode != "2":
                    print("\t\t\tInvalid value!")
                    mode = input(
                        "\t\t\tPlease choose the mode:\n\t\t\t1-One player mode\n\t\t\t2-Two players mode\n\t\t\t>>>")
                # ---------------------------------------------------------------------------------------------------- #
                # ----------------------------------------ONE PLAYER MODE--------------------------------------------- #
                # ---------------------------------------------------------------------------------------------------- #
                if mode == "1":
                    player = OM.OnePlayerMode()
                    puzzle = player.random(level)
                    # save the starting time to use it in the total score
                    startingTime = time()
                    player.printTable(puzzle)
                    # ask the player to choose a game option (fill, hint, or solve)
                    print("\t\t\tChoose an option:")
                    print("\t\t\tF: Fill\n\t\t\tH: Hint (you will lose 2 points)\n\t\t\tS: Solve")
                    gameOption = input("\t\t\t>>>")
                    # if the option is "S", the game will end
                    while gameOption != "S":
                        # if the puzzle is solved, the game will end
                        checkIfSolved = 0 not in puzzle
                        if checkIfSolved:
                            print("\t\t\tThe puzzle is already solved!")
                            break
                        # if the option is "F" then the player will fill one cell, if the value is right,
                        # then the player will gain 1 point. If it's not, then he will lose 1 point
                        if gameOption == "F":
                            player.fill(puzzle)
                        # if the option is "H" then one cell will be solved, and the player will lose 2 points
                        elif gameOption == "H":
                            player.hint(puzzle)
                        else:
                            print("\t\t\tInvalid value!!")
                        print("\t\t\tChoose an option:")
                        print("\t\t\tF: Fill\n\t\t\tH: Hint (you will lose 2 points)\n\t\t\tS: Solve")
                        gameOption = input("\t\t\t>>>")
                    # the total time is equal the end time - starting time
                    totalTime = time() - startingTime
                    # calculate the total score after ending the game
                    scores = player.calculateScores(totalTime)
                    print(f"\t\t\tYour total score is : {scores}")
                    player.solve(puzzle)
                    player.printTable(puzzle)
                # ---------------------------------------------------------------------------------------------------- #
                # ----------------------------------------TWO PLAYERS MODE-------------------------------------------- #
                # ---------------------------------------------------------------------------------------------------- #
                else:
                    playerNumber = 0
                    player1 = TM.TwoPlayersMode()
                    player2 = TM.TwoPlayersMode()
                    puzzle = SudokuGame.Sudoku.random(level)
                    # these variables to save the total time for each player
                    totalTime1 = totalTime2 = 0
                    startingTime = time()
                    SudokuGame.Sudoku.printTable(puzzle)
                    # ask the player to choose a game option (fill, pass, or solve)
                    print(f"\t\t\tPlayer{playerNumber+1} turn")
                    print("\t\t\tChoose an option:")
                    print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                    gameOption = input("\t\t\t>>>")
                    noPass = 0
                    # if the option is "S" the game will end
                    while gameOption != "S":
                        # if the puzzle is solved, the game will end
                        checkIfSolved = 0 not in puzzle
                        if checkIfSolved:
                            print("\t\t\tThe puzzle is already solved!")
                            break
                        # ---------------------------------------Player1---------------------------------------------- #
                        if playerNumber == 0:
                            # if the option is "F" then the player will fill one cell, if the value is right,
                            # then the player will gain 1 point. If it's not, then he will lose 1 point
                            if gameOption == "F":
                                player1.fill(puzzle)
                                # reset noPass (we have to check if the four passes are sequentially)
                                noPass = 0
                            # if the option is "P" then the turn will be for the other play
                            elif gameOption == "P":
                                noPass += 1
                                player1.setPoints(player1.getPoints() - 1)
                                # after four passes (in sequence) the game will display a hint
                                if noPass == 4:
                                    noPass = 0
                                    print("\t\t\t\t\t HINT:")
                                    player1.hint(puzzle)
                                else:
                                    player1.printTable(puzzle)
                            else:
                                print("\t\t\tInvalid option!!")
                                print(f"\t\t\tPlayer{playerNumber+1} turn")
                                print("\t\t\tChoose an option:")
                                print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                                gameOption = input("\t\t\t>>>")
                                continue
                            # after finishing the player's turn,
                            # the time was spend in this turn will be added to the total time
                            totalTime1 += time() - startingTime
                            # the starting time for other player
                            startingTime = time()
                        # ---------------------------------------Player2---------------------------------------------- #
                        elif playerNumber == 1:
                            if gameOption == "F":
                                # if the option is "F" then the player will fill one cell, if the value is right,
                                # then the player will gain 1 point. If it's not, then he will lose 1 point
                                player2.fill(puzzle)
                                # reset noPass (we have to check if the four passes are sequentially)
                                noPass = 0
                                # if the option is "P" then the turn will be for the other player
                            elif gameOption == "P":
                                player2.setPoints(player2.getPoints() - 1)
                                noPass += 1
                                # after four passes (in sequence) the game will display a hint
                                if noPass == 4:
                                    noPass = 0
                                    print("\t\t\tHINT:")
                                    player2.hint(puzzle)
                                else:
                                    player2.printTable(puzzle)
                            else:
                                print("\t\t\tInvalid option!!")
                                print(f"\t\t\tPlayer{playerNumber+1} turn")
                                print("\t\t\tChoose an option:")
                                print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                                gameOption = input("\t\t\t>>>")
                                continue
                            # after finishing the player's turn,
                            # the time was spend in this turn will be added to the total time
                            totalTime2 += time() - startingTime
                            startingTime = time()
                        # the roles are switched between players
                        playerNumber = (playerNumber + 1) % 2
                        print(f"\t\t\tPlayer{playerNumber+1} turn")
                        print("\t\t\tChoose an option:")
                        print("\t\t\tF: Fill\n\t\t\tP: Pass(you will lose 1 point)\n\t\t\tS: Solve")
                        gameOption = input("\t\t\t>>>")
                    # after ending the game, the player who ended the game,
                    # the time will be added to the total time of him
                    if playerNumber == 0:
                        totalTime1 += time() - startingTime
                        startingTime = time()
                    else:
                        totalTime2 += time() - startingTime
                        startingTime = time()
                    # at the end of the game, the scores will be calculated
                    scores1 = player1.calculateScores(totalTime1, totalTime2)
                    scores2 = player2.calculateScores(totalTime2, totalTime1)
                    print("\t\t\tThe player1 total score is:", scores1)
                    print("\t\t\tThe player2 total score is:", scores2)
                    SudokuGame.Sudoku.solve(puzzle)
                    SudokuGame.Sudoku.printTable(puzzle)
            break
        else:
            print("\t\t\tInvalid value!")
            print("\t\t\t1- load a puzzle from a text file")
            print("\t\t\t2- start a random puzzle")
            option = input("\t\t\t>>>")
    print("\t\t\tGood bye ^-^")
