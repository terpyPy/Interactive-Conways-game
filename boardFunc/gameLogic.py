#!/usr/bin/python3
# ----------------------------------------------------------------------------------------------------------------------
#  Author:      Cameron Kerley & Hunter Hannula (terpyPY: https://github.com/terpyPy/Interactive-Conways-game)
#               Hunter contributed the following code:
#                   1. created the gameLogic functionality for the light control logic.
#                   2. provided the concept of a playable game of life, initially only 4 neighbors were inverted on press.
#  Description: This is the game logic for the game of life &
#               the lights out game that terpyPY updated from micro-python and ported from a Trinket-M0 board.
#               the game now uses an eight neighbor adjacency algorithm for both applications, game & simulation.
#               The game of life is a cellular automaton that is a 2D array of cells
#               written to only evaluate the off color so that the on-color can be any RGB value tuple (255,255,255).
# -----------------------------------------------------------------------------------------------------------------------
#  Date:        6 June 2022
#  License:     MIT License
#
#  Disclosure:  This code is public domain. You can use it in any way you want.
#               However, i am scanning github repos for this code that does not include credit to me.
#               I have left some patterns in the naming convention and access methods
#               in this project making copy/pasted stolen code easy to parse and find.
from . import funcTest


def gameLogic(theBoard, event, onColor, offColor):
    #
    # get the 1d event button mapping for grid
    col, row = event
    #
    # algorithm corresponding 8 neighbor cell calc
    neighbors = funcTest.eight_neighbors_adj(theBoard, col, row)
    #
    #  unpack the column and row values calc from neighbors y,x orientation to match how board is drawn.
    for x, y in neighbors:
        # first check if the neighbor in the list is off on the game board
        if theBoard[x][y] == offColor:
            # if its not turned on turn y=the light on
            theBoard[x][y] = onColor
        # elif the neighbor cell is not eqaul to the off color thens its turned on
        else:
            # so we turn it off it the prevouis isnt true
            theBoard[x][y] = offColor
    # turn off the pressed key
    theBoard[col][row] = offColor
    # return the new board
    return theBoard
# -----------------------------------------------------------------------------------------------------------------------
# Author = Cameron Kerley/"terpyPY"
# inspired by collaboration with Hunter Hannula on our micro-python puzzle game "Lights Out"


def NewGameLogic(theBoard: set, 
                 event: tuple, 
                 onColor: tuple, 
                 offColor: tuple,
                 *rules):
    # these are order as the comparisons are made,
    # meaning that explicit order is ---> "if 'rule1' and 'rule2':" ect.
    if len(rules) > 0:
        gameRules = [int(rule) for rule in rules]
    else:
        gameRules = [3,4,6]
    
    numOff = 0
    numOn = 0
    # get the 1d event button mapping for grid
    col, row = event
    # print(row, col)
    #
    # algorithm corresponding 8 neighbor cell calc
    neighbors = funcTest.eight_neighbors_adj(theBoard, col, row)
    #
    # unpack the column and row values calc from neighbors
    # y,x orientation to match how board is drawn.
    for x, y in neighbors:
        # first check if the neighbor in the list is off on the game board
        if theBoard[x][y] == offColor:
            # if its not turned on turn y=the light on
            numOff += 1
        # elif the neighbor cell is not eqaul to the off color thens its turned on
        else:
            # so we turn it off it the prevouis isnt true
            numOn += 1
    # turn off the pressed key
    effectedNeighors = []
    for x, y in neighbors:
        
        if numOff < gameRules[0] or numOn-numOff > gameRules[1]:
            effectedNeighors.append((x, y))
            theBoard[x][y] = offColor
        if numOn == gameRules[2]:
            effectedNeighors.append((x, y))
            theBoard[x][y] = onColor
    # return the new board
    return theBoard, effectedNeighors
