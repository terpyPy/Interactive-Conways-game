#!/usr/bin/python3
#
#  Author:      Cameron Kerley (terpyPY: https://github.com/terpyPy/Interactive-Conways-game)
#  Date:        6 June 2022
#  License:     MIT License
#  description: This is the main file for what makes up one base entity the grid overly for the tileGroup.
#----------------------------------------------------------------------------------------------------------------------
#  Disclosure:  This code is public domain. You can use it in any way you want. 
#               However, i am scanning github repos for this code that does not include credit to me. 
#               I have left some patterns in the naming convention and access methods
#               in this project making copy/pasted stolen code easy to parse and find.
#
import pygame
import os
# from lib.baseEntityFlags import objGroup_flags
resourcPath = os.path.join(
                    os.environ.get("_MEIPASS2", os.path.abspath(".")),'images\\gridTile.bmp')
class Grid:

    def __init__(self, screen, rect=[], cords=(), settings={},noPad=False):
        #init the tile and set its position                                                       
        #in pygame the origin is (0,0) at the top lft of the screen. cords > 0 for x -> right, y 0___> +x and <= 1200
        #                                                                                        |
                                                                                           #     v +y and <= 800
        # 
        self.noPad = noPad
        self.screen = screen
        self.screen_rect = rect
        self.leftFromCenter_pad = settings.get_grid_padding()
        self.Entity_pointer = cords
        #default image size is 50
        self.DEFAULT_SIZE = settings.DEFAULT_SIZE_IMG
        # load the tile and get its rectangle
        '''when working with rect you can use (x,y) 
        of top,bot,midlft,rght to place object'''
        img = pygame.image.load(resourcPath)
        # self.h = self.DEFAULT_SIZE[0] - settings.N//0.5
        # if self.h <= 10:
        self.h = ((settings.screen_height-self.DEFAULT_SIZE[0])//(settings.N))
        self.w = (((settings.screen_height-self.DEFAULT_SIZE[0])-5)//(settings.N))
        self.image = pygame.transform.scale(img, (int(self.w), int(self.h)))
        # get image rect
        self.rect = self.image.get_rect()
        # set the tile's x position with the cords provided.
        self.setPad(cords)
        # set the tile's y position with the cords provided.
        #place tile at bottom center of screen
        
    def setPad(self, cords:tuple):
        if self.noPad is True:
            self.rect.x = (cords[0]*self.h)
        else:
            self.rect.x = (cords[0]*self.h)+self.leftFromCenter_pad
            
        self.rect.y = (cords[1]*self.h)+5
        
    def get_img_size(self):
        return self.h
    
    def get_pointer(self):
        return self.Entity_pointer
    
    def blitme(self):
        # draw the ship at its current location
        self.screen.blit(self.image,self.rect)
