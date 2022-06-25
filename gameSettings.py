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
class Settings:
    # store the game settings
    def __init__(self, screen:tuple=(0,0), isGlobal:str=False) -> object:
        # screen settings
        self.screen_width, self.screen_hight = screen
        
        if isGlobal == True:
            if screen == (0,0):
                print('used default screen size')
            else:
                print(f'screen_width :{self.screen_width}\n screen_hight: {self.screen_hight}')
        else:
            print(f'no screen settings used for _{isGlobal}_')
        self.bg_color = (40,40,40)
        # game driver settings
        self.isMulticolor = False
        self.isPause = False
        self.modes = ['run', 'draw', 'nGame']
        self.mode = 'start'
        self.onColor = (0,114,160)
        self.offColor = (250,250,250)
        self.winColor = (0, 25, 0)
        self.simColor = (10, 93, 30)
        self.DEFAULT_SIZE_IMG = (60,60)