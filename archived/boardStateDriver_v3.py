#!/usr/bin/env python3
import boardFunc
import cpuEvaluate
from time import monotonic
from random import randrange

# DONE: we need a way to copy just the colors at each index of the board, and return it, 
''' modified:'''
    # -the board logic comprehension 
    # -and gamlogic back to only takeing an array of RGB tuples
class boardState():

    def __init__(self, state):# this would need to take
        self.isMulticolor = False
        self.isPause = False
        self.state = state 
        self.onColor = (250,0,0)
        self.offColor = (250,250,250)
        self.winColor = (0, 25, 0)
        self.simColor = (10, 93, 30)
        self.N = self.state.N
        self.colorList = [[None]*self.N for _ in range(self.N)]
        self.emptyBoard = [[(self.offColor)]*self.N for button in range(self.N)]
        self.winBoard = [[(self.winColor)]*self.N for button in range(self.N)]
        self.theBoard = [[None]*self.N for _ in range(self.N)]# the init method takes one argument, the grid size
        self.timePressed = monotonic()
        self.eventButt = None
        self.previousButtonPressed = ()
        self.mode = 'start'
        self.cpuState = 'min'

    def debounce(self):
        # filters button inputs, input will only be accepted every 0.2 seconds as measured from last press
        if monotonic() - self.timePressed > 0:
            return True
        else:
            return False 
    
    def color_list(self):
        colorList = self.colorList.copy()
        for i in range(self.N):
            for j in range(self.N):
                 colorList[i][j] = self.theBoard[i][j].Color
        return colorList    
    
    def update_color(self, colors):
        for i in range(self.N):
            for j in range(self.N):
                self.theBoard[i][j].Color  = colors[i][j] 
        
    def animation(self):
        # this function runs the game in a way where each button press is random
        # and the color is as well, and it uses the real game anb board logic to produce an animation.
        if not self.isPause:
                if self.isMulticolor:
                    self.onColor = (randrange(0,254),randrange(27,254),randrange(0,254))
                simPress = (randrange(0,self.N),randrange(0,self.N))
                self.boardLogic(simPress)
                # boardInstance = self.color_list()
            
                # if self.cpuState == 'min':
                #     simPress = cpuEvaluate.findBestMove(boardInstance, self.offColor, self.previousButtonPressed)
                #     self.cpuState = 'max'
                # elif self.cpuState == 'max':
                #     simPress = cpuEvaluate.findBestMove(boardInstance, self.onColor, self.previousButtonPressed)
                #     self.cpuState = 'min'
                # # print(self.cpuState)
                # self.boardLogic((simPress[0],simPress[1]))
                
    def choseMode(self):
            self.theBoard[0][0].Color = self.onColor
            self.theBoard[1][0].Color = self.simColor
            self.theBoard[2][0].Color = (123,30,170)
            if self.eventButt == (0,0):
                self.mode = 'run'
                self.clearBoard()
            elif self.eventButt == (1,0):
                # event = 1
                self.mode = 'sim'
                self.clearBoard()
            elif self.eventButt == (2,0):
                self.mode = 'draw'
                self.clearBoard()
            # self.eventButt = None
            elif self.eventButt == (3,0):
                self.mode = 'nGame'
                self.clearBoard()

    def randomStart(self):
        for i in range(self.N):
            for j in range(self.N):
                self.previousButtonPressed = (randrange(0,self.N), randrange(0,self.N))
                boardInstance = self.color_list()
                boardInstance = boardFunc.gameLogic(boardInstance,
                                                    self.previousButtonPressed,
                                                    self.onColor,
                                                    self.offColor)
                self.update_color(boardInstance)
                self.previousButtonPressed = ()

    def clearBoard(self):
        self.previousButtonPressed = None
        self.eventButt = (self.N,0)
        # list of tiles in the off state to give as arg for update color
        
        self.update_color(self.emptyBoard)
       
        if self.mode == 'run':        
            self.randomStart()
        elif self.mode == 'sim':
            self.randomStart()
        elif self.mode == 'nGame':
            self.randomStart()
            
    def boardLogic(self, event):
       
        if self.mode != 'sim':
            self.eventButt = event
        else:
            self.eventButt = event
       
        if self.debounce():
           
            if not self.eventButt == self.previousButtonPressed:
                print(event)
                self.previousButtonPressed = self.eventButt
                
                # create a reference to the current state of the button colors
                boardInstance = self.color_list()
                if self.mode == 'nGame':
                    boardInstance = boardFunc.NewGameLogic(boardInstance,
                                                    self.eventButt,
                                                    self.onColor,
                                                    self.offColor)
                else:
                    boardInstance = boardFunc.gameLogic(boardInstance,
                                                    self.eventButt,
                                                    self.onColor,
                                                    self.offColor)
                #pass the updated color pointers to the entity list
                self.update_color(boardInstance)
                if (self.mode != 'draw') or (self.mode != 'nGame'):
                # if the mode flag isnt set to draw check the win condition
                    if boardFunc.funcTest.checkWin(boardInstance, self.N):
                        self.update_color(self.winBoard)
                        print('you won')
            else:
                print('debounce failed')
                                    
            self.timePressed = monotonic()
