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
        super().__init__(state.N, isGlobal='boardState.py')
        self.N = state.N
        self.colorList = [[None]*self.N for _ in range(self.N)]
        self.emptyBoard = [
            [(self.offColor)]*self.N for button in range(self.N)]
        self.winBoard = [[(self.winColor)]*self.N for button in range(self.N)]
        # the init method takes one argument, the grid size
        self.theBoard = state.board.tileArray
        self.sateGet = state.board
        self.buttonsToColor = [self.theBoard[0][0],
                               self.theBoard[1][0],
                               self.theBoard[2][0],
                               self.theBoard[3][0]]
        self.timePressed = monotonic()
        self.eventButt = None
        self.previousButtonPressed = ()
        self.changedIndexes = []
        self.isWin = False
        self.rules = (3, 6, 4)
        self.lastTwo = []

    def resetDriver(self):
        self.colorList.clear()
        self.emptyBoard.clear()
        self.theBoard.clear()

    def getMode(self):
        return self.mode

    def debounce(self):
        # filters button inputs, input will only be accepted every 0.2 seconds as measured from last press
        if monotonic() - self.timePressed > 0:
            return True
        else:
            return False

    def get_color_list(self):
        colorList = self.sateGet.getColors()
        return colorList

    def set_color_list(self, colors):
        self.sateGet.setColors(colors)
        

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
                    self.theBoard[i][j].isEffected += 1
                    x = self.theBoard[i][j].isEffected
                    # print(x)
                    onColor = ((x+i+j) % 250, (x*(i)+j) % 125, (x*(i+j)) % 250)
                simPress = (i, j)
                boardInstance, self.changedIndexes = boardFunc.NewGameLogic(boardInstance,
                                                                            simPress,
                                                                            onColor,
                                                                            self.offColor, *self.rules)
        return boardInstance

    def cpuPlay(self):
        pass

    def choseMode(self):
        if self.eventButt == None:
            self.buttonsToColor[0].Color = self.onColor
            self.buttonsToColor[1].Color = self.simColor
            self.buttonsToColor[2].Color = (123, 30, 170)
            self.buttonsToColor[3].Color = (50, 50, 170)
            print('on start screen')
        else:
            if self.eventButt != -2:
                if self.eventButt == (0, 0):
                    self.mode = self.modes[0]
                    self.clearBoard()

                elif self.eventButt == (1, 0):
                    self.mode = self.modes[1]
                    self.clearBoard()

                elif self.eventButt == (2, 0):
                    self.mode = self.modes[2]
                    self.clearBoard()

                elif self.eventButt == (3, 0):
                    self.mode = self.modes[3]
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

        if self.getMode() in ('run', 'AI'):
            self.randomStart()

    def boardLogic(self, event, *rules):

        if self.mode in self.modes:
            self.eventButt = event

            if not self.eventButt == self.previousButtonPressed:

                # create a reference to the current state of the button colors
                if self.getMode() == self.modes[2]:
                    boardInstance = self.get_color_list()
                    if not self.isPause:
                        boardInstance = self.animation(boardInstance)
                        # time.sleep(0.08)
                    elif rules:
                        self.rules = rules[0]
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

                    if self.getMode() != self.modes[1]:
                        # if the mode flag isnt set to draw check the win condition
                        if boardFunc.funcTest.checkWin(boardInstance, self.N):
                            self.set_color_list(self.winBoard)
                            self.isWin = True
                            print('you won')
            else:
                print('debounce failed')

            self.timePressed = monotonic()
        else:
            self.choseMode()
            self.eventButt = event
