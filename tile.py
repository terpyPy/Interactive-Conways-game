#!/usr/bin/env python3
import pygame, pygame.display
from deBugTiles import tileWindow
from lib.baseEntityFlags import objGroup_flags
from grid import Grid
class Tile:

    def __init__(self, screen:pygame.display, rect, n,cords, currSize):
        #init the tile and set its position                                                       
        #in pygame the origin is (0,0) at the top lft of the screen. cords > 0 for x -> right, y 0___> +x and <= 1200
        #                                                                                        |
                                                                                           #     v +y and <= 800
        self.screen = screen
        self.screen_rect = rect
        self.leftFromCenter_pad = int(self.screen_rect.center[0]*0.62) - n
        
        #default image size is 50
        self.DEFAULT_SIZE = currSize
        # load the tile and get its rectangle
        '''when working with rect you can use (x,y) 
        of top,bot,midlft,rght to place object'''
        img = pygame.image.load('images/tile.bmp')
        scaleSize = self.DEFAULT_SIZE[0] - n//1.5
        if scaleSize < 19:
            scaleSize = 15
        self.image = pygame.transform.scale(img, (int(scaleSize),int(scaleSize)))
    
        self.rect = self.image.get_rect()
        self.rect.x = (cords[0]*scaleSize)+self.leftFromCenter_pad
        self.rect.y = (cords[1]*scaleSize)+5
        #place tile at bottom center of screen
        self.Color = (250,250,250)
        self.isEffected = 1
        self.textWindow = tileWindow(self,self.isEffected,self.rect.x,self.rect.y)

    def blitme(self, debug):
        # draw the obj at its current location
        self.image.fill(self.Color)
        self.screen.blit(self.image,(self.rect.x, self.rect.y))
        if debug and self.Color != ((250,250,250)):         
            self.textWindow.blitme(self.isEffected)
    
class tileGroup(objGroup_flags):
    def __init__(self, state, *args) -> None:
        # initialize the flags object with the flags passed in
        super().__init__(*args)
        
        self.screen = state.screen
        self.screen_rect = state.screen.get_rect()
        self.N = state.N
        self.DEFAULT_SIZE = state.settings.DEFAULT_SIZE_IMG
        # check if there are any flags passed into the constructor
        for flag in self.flags:
            if flag == 'testMode':
                self.alphaN = flag
                self.tileArray = [
                    [Tile(
                        self.screen,
                        self.screen_rect,
                        self.alphaN,
                        (i,j), 
                        self.DEFAULT_SIZE
                        ) 
                    for i in range(self.alphaN)] 
                    for j in range(self.alphaN)]
                
                self.gridArray = [
                    [Grid(self.screen,
                                    self.screen_rect,
                                    self.alphaN,
                                    (i,j),
                                    self.DEFAULT_SIZE) 
                            for i in range(self.alphaN)]
                            for j in range(self.alphaN)]
                break
                
        else:
            self.tileArray = [
            [Tile(
                self.screen,
                self.screen_rect,
                self.N,
                (i,j),
                self.DEFAULT_SIZE
                )
            for i in range(self.N)]
                for j in range(self.N)]
            self.gridArray = [
                [Grid(self.screen,
                                    self.screen_rect,
                                    self.N,
                                    (i,j),
                                    self.DEFAULT_SIZE) 
                                for i in range(self.N)]
                                for j in range(self.N)]
                
    def getTextXY(self):
        x,y = [self.gridArray[0][self.N-1].rect.x, self.gridArray[0][self.N-1].rect.y]
        return x,y
        
    def drawTile(self,debug,i,j):
        self.tileArray[i][j].blitme(debug)
        self.gridArray[i][j].blitme()
    