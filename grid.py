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
# from lib.baseEntityFlags import objGroup_flags
class Grid:

    def __init__(self, screen, rect, n,cords, currSize):
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
        img = pygame.image.load('images/gridTile.bmp')
        scaleSize = self.DEFAULT_SIZE[0] - n//1.5
        if scaleSize < 19:
            scaleSize = 15
        
        self.image = pygame.transform.scale(img, (int(scaleSize),int(scaleSize)))
        self.rect = self.image.get_rect()
        self.rect.x = (cords[0]*scaleSize)+self.leftFromCenter_pad
        self.rect.y = (cords[1]*scaleSize)+5
        #place tile at bottom center of screen
    

    def blitme(self):
        # draw the ship at its current location
        self.screen.blit(self.image,self.rect)
