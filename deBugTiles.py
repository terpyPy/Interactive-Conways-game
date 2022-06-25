#!/usr/bin/python3
#
#  Author:      Cameron Kerley (terpyPY: https://github.com/terpyPy/Interactive-Conways-game)
#  Date:        6 June 2022
#  License:     MIT License
#
#  description: This is the one file for what makes up the the full tile entity.
#               responsible for overlaying the node activity on the grid when the "D" key is pressed.
#               Managed by and drawn to screen from the tileGroup class.
#----------------------------------------------------------------------------------------------------------------------
#  Disclosure:  This code is public domain. You can use it in any way you want. 
#               However, i am scanning github repos for this code that does not include credit to me. 
#               I have left some patterns in the naming convention and access methods
#               in this project making copy/pasted stolen code easy to parse and find.
import pygame
import os
class tileWindow:
    
    def __init__(self, state,n,x,y):
        self.msg = n
        self.screen = state.screen
        self.x = x+5
        self.y = y+5
        self.font = pygame.font.Font(os.path.join('pygame/', 'freesansbold.ttf'), 11)
    def blitme(self,msg):
        
        self.text = self.font.render(str(msg-1), True, (250,0,0), (250,250,250))
        self.screen.blit(self.text, (self.x, self.y))