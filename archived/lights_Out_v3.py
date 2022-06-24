#!/usr/bin/env python3
import time
from boardStateDriver import boardState
from gameSettings import Settings
import sys
import pygame
import pygame.display
import pygame.event
import pygame.mouse
from tile import Tile
from Grid import Grid

class LightsOutGame:
    # over all class to manage the game
    def __init__(self, N):
        self.N = N
        # init game and create screen game resource
        pygame.init()
        # make screen surface
        self.settings = Settings(N)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_hight))
        pygame.display.set_caption("lights out")
        
        # passing self gives the Tile obj a current instance of the state
        self.tile = boardState(self) # this becomes bsdrive
        # init an array of NxN dementions to mange the grid
        self.grid = [[None]*self.N for _ in range(self.N)] 
        for i in range(self.N):
            for j in range(self.N):
                self.tile.theBoard[i][j] = Tile(self,(i,j))
                self.grid[i][j] = Grid(self,(i,j))

    def run_game(self):
        while True:
            # self._update_screen()
            self._choose_mode()
            self._check_events()
            self._update_screen()
            # self.grid.blitme()
            if self.tile.theBoard[0][0].Color == self.tile.winColor:
                time.sleep(2)
                self.tile.clearBoard()
        
    def _choose_mode(self):
        if self.tile.mode == 'start':
            self.tile.choseMode()
        elif self.tile.mode == 'sim':
            self.tile.animation()
        elif self.tile.mode == 'nGame':
            self.tile.animation()

    def _check_events(self):
        # key listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                try:
                    i,j = self._get_button_click(x,y)
                    self.tile.boardLogic((i,j))
                except TypeError:
                    continue
            elif event.type == pygame.KEYDOWN:
                # if an arrow key is pressed check its mapping to its menu option,
                self._menu_Keys(event.key)
                
    def _get_button_click(self,x,y):
        for i in range(len(self.tile.theBoard)):
            for j in range(len(self.tile.theBoard)):
                # find the location that the click was on a valid tile     
                if self.tile.theBoard[i][j].rect.collidepoint(x, y):
                    print(x,y,(i,j))
                    # return the correct tile location in the array
                    return (i,j)

    def _menu_Keys(self,eventKey:int):
        # start from a fresh board of the given menu option,
        # for chose mode eventbutton is set to 4,0 if more click-able menu options
        # must be changed
        if eventKey == pygame.K_LEFT:
            self.tile.mode = 'start'
            self.tile.clearBoard()
        elif eventKey == pygame.K_UP:
            self.tile.mode = 'sim'
            self.tile.clearBoard()
        elif eventKey == pygame.K_RIGHT:
            self.tile.mode = 'run'
            self.tile.clearBoard()
        elif eventKey == pygame.K_DOWN:
            self.tile.mode = 'draw'
            self.tile.clearBoard()
        elif eventKey == pygame.K_SPACE:
            self.tile.mode = 'nGame'
            self.tile.clearBoard()
        elif eventKey == pygame.K_c:
            if self.tile.isMulticolor:
                self.tile.isMulticolor = False
            else:
                self.tile.isMulticolor = True
            
        elif self.tile.mode != 'run':    
            if eventKey == pygame.K_1:
                self.tile.isPause = True
                # self.tile.clearBoard()
            elif eventKey == pygame.K_2:
                self.tile.isPause = False
            # self.tile.animation()
                
    def _update_screen(self):
        # redraw screen surface ea loop
        self.screen.fill(self.settings.bg_color)
        # draw the tiles on top of the screen
        
        for i in range(self.N):
            for j in range(self.N):
                self.tile.theBoard[i][j].image.fill(self.tile.theBoard[i][j].Color)
                self.tile.theBoard[i][j].blitme()
                self.grid[i][j].blitme()
        # make most recent drawn screen appear
        pygame.display.flip()

if __name__ == '__main__':
    state = LightsOutGame(15)
    state.run_game()
