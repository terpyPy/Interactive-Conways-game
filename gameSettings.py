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
import pygame

class Settings:
    # store the game settings
    def __init__(self, N:int,screen:tuple=(0,0), isGlobal:str=False) -> object:
        # screen settings
        self.screen_width, self.screen_height = screen
        self.N = N
        self.animation_FPS = 5
        if isGlobal == True:
            if screen == (0,0):
                print('used default screen size')
            else:
                print(f'screen_width :{self.screen_width}\n screen_hight: {self.screen_height}')
        else:
            print(f'not screen settings for isGlobal. \nused {self.screen_width}:{self.screen_height}')
        self.bg_color = (40,40,40)
        # game driver settings
        self.isMulticolor = False
        self.isPause = False
        self.modes = ['run', 'draw', 'nGame',"AI"]
        self.mode = 'start'
        self.menuKeys = {pygame.K_RIGHT: 'run',
                    pygame.K_DOWN: 'draw',
                    pygame.K_UP: 'nGame',
                    pygame.K_LEFT: 'start',
                    }
        self.pauseKeys = {pygame.K_a: self.isPause,
                            pygame.K_RETURN: (-2, False),}
        self.onColor = [0,114,160]
        self.offColor = [50,50,50]
        self.winColor = [0, 25, 0]
        self.simColor = [10, 93, 30]
        self.DEFAULT_SIZE_IMG = (60,60)
        
    def get_grid_padding(self) -> tuple:
        return int(60)
    
    def get_temp_path(self) -> str:
        return r"D:\2021code\NumpyAnimation\images\temp.bmp"
