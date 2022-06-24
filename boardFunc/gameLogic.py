#!/usr/bin/env python3

from . import funcTest
def gameLogic(theBoard, event, onColor, offColor):
    #
    # get the 1d event button mapping for grid
    row, col = event
    #
    # algorithm corresponding 8 neighbor cell calc
    neighbors = funcTest.neighbors(theBoard, row,col)
    #
    #  unpack the column and row values calc from neighbors y,x orientation to match how board is drawn.
    for x ,y in neighbors:
        # first check if the neighbor in the list is off on the game board
        if theBoard[x][y] == offColor:
            # if its not turned on turn y=the light on
            theBoard[x][y] = onColor
        # elif the neighbor cell is not eqaul to the off color thens its turned on
        elif theBoard[x][y] != offColor:
            # so we turn it off it the prevouis isnt true
            theBoard[x][y] = offColor
    # turn off the pressed key
    theBoard[row][col] = offColor
    # return the new board
    return theBoard

def NewGameLogic(theBoard:set, event:tuple, onColor:tuple, offColor:tuple):
    numOff = 0
    numOn = 0
    # get the 1d event button mapping for grid
    row, col = event
    # print(row, col)
    #
    # algorithm corresponding 8 neighbor cell calc
    neighbors = funcTest.neighbors(theBoard, row,col)
    #
    #  unpack the column and row values calc from neighbors y,x orientation to match how board is drawn.
    for x ,y in neighbors:
        # first check if the neighbor in the list is off on the game board
        if theBoard[x][y] == offColor:
            # if its not turned on turn y=the light on
            numOff +=1
        # elif the neighbor cell is not eqaul to the off color thens its turned on
        elif theBoard[x][y] != offColor:
            # so we turn it off it the prevouis isnt true
            numOn += 1
    # turn off the pressed key
    effectedNeighors = []
    for x ,y in neighbors:
        if numOff <= 4 and numOn-numOff  >=  5:
            effectedNeighors.append((x,y))
            theBoard[x][y] = offColor
            numOff += 1
            numOn -=1
        elif numOn  <=  4 and numOff-numOn <= 3:
            effectedNeighors.append((x,y))
            theBoard[x][y] = onColor
            numOn += 1
            numOff -=1
        # else:
        #     if (numOff + numOn) == y:
        #         effectedNeighors.append((numOff,y))
        #         theBoard[numOff][y] = offColor
        #     elif (numOff + numOn) == x:
        #         effectedNeighors.append((x, numOn))
        #         theBoard[x][numOn] = onColor  
        # return the new board
    return theBoard, effectedNeighors