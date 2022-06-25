#!/usr/bin/python3
#
#  Author:      Cameron Kerley (terpyPY: https://github.com/terpyPy/Interactive-Conways-game)
#  Date:        6 June 2022
#  License:     MIT License
#
#  Disclosure:  This code is public domain. You can use it in any way you want. 
#               However, i am scanning github repos for this code that does not include credit to me. 
#               I have left some patterns in the naming convention and access methods
#               in this project making copy/pasted stolen code easy to parse and find.
#
import time
import boardFunc
from time import monotonic
from random import randrange
# from lib.baseEntityFlags import objGroup_flags
from gameSettings import Settings

# DONE: we need a way to copy just the colors at each index of the board, and return it,
''' modified:'''
# -the board logic comprehension
# -and gamlogic back to only takeing an array of RGB tuples


class boardState(Settings):

    def __init__(self, state, *args):
        # inherited instance of Settings from the game settings class
        super().__init__(isGlobal='boardState.py')
        self.N = state.N
        self.colorList = [[None]*self.N for _ in range(self.N)]
        self.emptyBoard = [
            [(self.offColor)]*self.N for button in range(self.N)]
        self.winBoard = [[(self.winColor)]*self.N for button in range(self.N)]
        # the init method takes one argument, the grid size
        self.theBoard = state.board.tileArray
        self.buttonsToColor = [self.theBoard[0][0],
                               self.theBoard[0][1],
                               self.theBoard[0][2]]
        self.timePressed = monotonic()
        self.eventButt = None
        self.previousButtonPressed = ()
        self.changedIndexes = []

    def debounce(self):
        # filters button inputs, input will only be accepted every 0.2 seconds as measured from last press
        if monotonic() - self.timePressed > 0:
            return True
        else:
            return False

    def get_color_list(self):
        colorList = self.colorList.copy()
        for i in range(self.N):
            for j in range(self.N):
                colorList[i][j] = self.theBoard[i][j].Color
        return colorList

    def set_color_list(self, colors):
        for i in range(self.N):
            for j in range(self.N):
                self.theBoard[i][j].Color = colors[i][j]

    def returnEffected(self):
        for i, j in self.changedIndexes:
            self.theBoard[i][j].isEffected += 1
        # return self.changedIndexes

    def animation(self, boardInstance):
        # this function runs the game in a way where each button press is random
        # and the color is as well, and it uses the real game anb board logic to produce an animation.

        onColor = self.onColor
        for i in range(self.N):
            for j in range(self.N):
                if self.isMulticolor:
                    x = self.theBoard[i][j].isEffected
                    # print(x)
                    onColor = ((100+i+j)%250, (x*(i)+j) % 125, (x*(i+j)) % 250)
                simPress = (i, j)
                boardInstance, self.changedIndexes = boardFunc.NewGameLogic(boardInstance,
                                                                            simPress,
                                                                            onColor,
                                                                            self.offColor)
                self.returnEffected()

        return boardInstance

    def choseMode(self):
        if self.eventButt == None:
            self.buttonsToColor[0].Color = self.onColor
            self.buttonsToColor[1].Color = self.simColor
            self.buttonsToColor[2].Color = (123, 30, 170)
            print('on start screen')
        else:
            if self.eventButt == (0, 0):
                self.mode = self.modes[0]
                self.clearBoard()

            elif self.eventButt == (0, 1):
                self.mode = self.modes[1]
                self.clearBoard()

            elif self.eventButt == (0, 2):
                self.mode = self.modes[2]
                self.clearBoard()
            # self.eventButt = None

    def randomStart(self):
        boardInstance = self.get_color_list()
        for i in range(self.N):
            for j in range(self.N):
                self.previousButtonPressed = (
                    randrange(0, self.N), randrange(0, self.N))

                boardInstance = boardFunc.gameLogic(boardInstance,
                                                    self.previousButtonPressed,
                                                    self.onColor,
                                                    self.offColor)
        self.set_color_list(boardInstance)
        self.previousButtonPressed = ()

    def clearBoard(self):
        self.previousButtonPressed = None
        self.eventButt = None
        # list of tiles in the off state to give as arg for update color
        self.set_color_list(self.emptyBoard)

        if self.mode == 'run':
            self.randomStart()

    def boardLogic(self, event):

        if self.mode in self.modes:
            self.eventButt = event

            if not self.eventButt == self.previousButtonPressed:

                # create a reference to the current state of the button colors
                if self.mode == self.modes[2] and not self.isPause:
                    boardInstance = self.get_color_list()
                    time.sleep(0.23)
                    boardInstance = self.animation(boardInstance)

                    self.set_color_list(boardInstance)

                if event not in (-1, -2):
                    print('event: ', self.eventButt)
                    boardInstance = self.get_color_list()
                    self.previousButtonPressed = self.eventButt
                    boardInstance = boardFunc.gameLogic(boardInstance,
                                                        self.eventButt,
                                                        self.onColor,
                                                        self.offColor)
                    self.set_color_list(boardInstance)
                # pass the updated color pointers to the entity list

                    if self.mode != self.modes[1]:
                        # if the mode flag isnt set to draw check the win condition
                        if boardFunc.funcTest.checkWin(boardInstance, self.N):
                            self.set_color_list(self.winBoard)
                            print('you won')
            else:
                print('debounce failed')

            self.timePressed = monotonic()
        else:
            self.choseMode()
            self.eventButt = event
