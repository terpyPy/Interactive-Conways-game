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
#  Description: pygame version of Conway's Game of Life and a puzzle game the uses
#               the neighbor adjacency rule to invert the colors of the tiles, 
#               with the goal to turn off all tiles. finally a drawing on the board option,
#               to set custom starting board states.
#
from lib.baseEntityFlags import objGroup_flags
import time
from boardStateDriver import boardState
from gameSettings import Settings
import sys
import pygame
import pygame.display
import pygame.event
import pygame.mouse
from tile import tileGroup
import pygame_textinput


class LightsOutGame(objGroup_flags):
    # over all class to manage the game
    def __init__(self, N:int, *args)->object:
        # init game and create screen game resource
        pygame.init()
        self.isDebugActivity = False
        self.keys = {pygame.K_RIGHT: 'run',
                pygame.K_DOWN: 'draw',
                pygame.K_SPACE: 'nGame',
                pygame.K_LEFT: 'start',
               }
        # N is either NxN grid or *args is a list of modifiers
        self.N = N
        self.alphaN = None
        # to get 2 rows and 4 cols, use argsIn for row, and self.N for col 
        # i.e (argsIn[0]:row, self.N:col)
        # rowSize = argsIn[0]
        # colSize = self.N
        # check optional args
        if len(args) > 0:
            argsToSub = list(filter(lambda x: str(x) != '', args))[0]
            super().__init__(argsToSub)
            self.alphaN = self.flags[0]
            # init the UI, N is passed to size the list comprehinsion,
            # was written to allow rebuilding the game in any NxN grid
            #
            # it may be best to create a new method to make the board UI,
            # when not creating NxN grid, but instead a custom grid.
            self.create_board_UI(self.alphaN) 
            #
        else:
            super().__init__()
            # init the UI, N is passed to size the list comprehinsion,
            # was written to allow rebuilding the game in any NxN grid
            self.create_board_UI()
       
        # init the UI, N is passed to size the list comprehinsion,
        # was written to allow rebuilding the game in any NxN grid
        # self.create_board_UI()
        # this library makes having user type box easy, not good
        self.textinput = pygame_textinput.TextInputVisualizer()
        # set the clock for pygame this will be used to synchronize 
        # the frames of the text box courser
        self.clock = pygame.time.Clock()

    def create_board_UI(self, *args):
        # this becomes bsdrive
        if self.alphaN is None:
            """TODO: make all this functions dependent on this function take *args 
            this allows for proper board size creation in window & on the fly reshaping."""
            # make screen surface
            
            self.screen = pygame.display.set_mode(
            (0,0), pygame.FULLSCREEN)
            pygame.display.set_caption("lights out")
            self.settings = Settings(screen=(self.screen.get_rect().center[0], self.screen.get_rect().center[1]), isGlobal=True)
            # init the grid drawn over each tile
            #
            """TODO: refactor constructor modifier class to allow for reshaping of the grid
            globally, not just the tile group & grid group I.E should update with board driver
            best thing to do is make a method to resize the grid group and tile group and use this to resize the board"""
            s='test'#for testing todo. remove after testing
            self.board = tileGroup(self)
            # self.grid = gridGroup(self)
            # passing self gives the Tile obj a current instance of the state
            self.driver = boardState(self)
            
            x,y = self.board.getTextXY()      
            self.texWincord1 = 500
            self.texWincord2 = x/2
    
    def windPrompt(self):
        '''should use the logic applied in this function 
        to enter custom & random board sizes and shapes'''
        if self.textinput.value.isdigit():
            self.N = int(self.textinput.value)
            self.create_board_UI()
        self.textinput.value = ''
        self.driver.mode = 'start'
                
    def run_game(self):
        # this is the event loop for the UI, 
        # 1) chose the play type
        # 2) check the events, ie button press on keyboard and the window
        # 3) draw the result of listening to the event or driver logic execution 
        while True:
            # 1
            self.driver.boardLogic(-2)
            # 2
            self._check_events()
            # 3
            self._update_screen()
            if self.driver.theBoard[0][0].Color == self.driver.winColor:
                time.sleep(2)
                self.driver.clearBoard()
        

    def _check_events(self):
        events = pygame.event.get()
        # wiki for this module said this is the way soo, give the text box ALL the events?
        # no way thats a good idea long term.
        
        self.textinput.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #
                x,y = event.pos
                # soo im just lazy and this works fine, for future, 
                # just compare the len(lst-1) before returning it, try returning -1,-1 on error
                try:
                    i,j = self._get_button_click(x,y)
                    self.driver.boardLogic((i,j))
                except TypeError:
                    print('not a valid tile')
                    continue
            elif event.type == pygame.KEYDOWN:
                # if an arrow key is pressed check its mapping to its menu option,
                self._menu_Keys(event.key)
                
    def _get_button_click(self,x,y):
        for i in range(len(self.driver.theBoard)):
            for j in range(len(self.driver.theBoard)):
                # find the location that the click was on a valid tile     
                if self.board.tileArray[i][j].rect.collidepoint(x, y):
                    print(x,y,(i,j))
                    # return the correct tile location in the array
                    return (i,j)

    def _menu_Keys(self,eventKey:int):
        # check if a key is pressed and change the mode accordingly
        #
        self.driver.mode = self.menuKeySwitcher(eventKey, self.driver.mode)
        # if not simulation mode clear the board on key press
        if self.driver.mode != 'nGame':
            if eventKey in self.keys.keys():
                self.driver.clearBoard()
                print(self.driver.mode)
            
        # move this into a function to isolate it.
        if eventKey == pygame.K_RETURN and self.driver.mode == 'start':
            self.windPrompt()
            
        # q to quit while running
        if eventKey == pygame.K_q:
            sys.exit()
        # toggle multicolors on key press
        if eventKey == pygame.K_c:
            # toggle colors on and off
            self.driver.isMulticolor = self.toggleColors()
            print(f'Debug_option-is-Multicolor_:-{self.driver.isMulticolor}') 
            
        if eventKey == pygame.K_d:
            # toggle debug mode on and off
            self.isDebugActivity = not self.isDebugActivity
            print(f'Debug_option-node-ACTIVITY_:-{self.isDebugActivity}')
            
        # toggle pause on key press
        if self.driver.mode in  ['run', 'nGame']:    
            # if the mode is not run, then the board state can be frozen
            self.driver.isPause = self.pauseFunc(eventKey)
               
    def menuKeySwitcher(self, event, mode):
        # take the event key and return the correct menu option
        if self.keys.get(event):
            return self.keys.get(event, mode)
        else:
            return mode
          
    def toggleColors(self):
        if self.driver.isMulticolor:
            return False
        else:
            return True
        
    def pauseFunc(self, event):
        if event == pygame.K_1:
            print(f'paused_simulation-: {True}')
            return True
            # self.tile.clearBoard()
        elif event == pygame.K_2:
            print(f'paused_simulation-: {not True}')
            return False
    
    def _update_screen(self):
        # redraw screen surface ea loop
        self.screen.fill(self.settings.bg_color)
        for i in range(self.N):
            for j in range(self.N):
                # draw the tiles & grid on top of the screen as a group.
                self.board.drawTile(self.isDebugActivity, i, j)
                
        # draw text input if start mode
        if self.driver.mode == 'start':
            self.screen.blit(self.textinput.surface, (self.texWincord1,self.texWincord2))
        # make most recent drawn screen appear
        pygame.display.flip()
        self.clock.tick(15)

if __name__ == '__main__':
    
    state = LightsOutGame(10)
    state.run_game()
