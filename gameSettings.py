class Settings:
    # store the game settings
    def __init__(self ,num:int,x=0, screen=(2560,1440)) -> object:
        # super(Settings, self).__init__()
        # screen settings
        self.screen_width, self.screen_hight = screen
        if x != 0:
            self.screen_width = 56*x
            self.screen_hight = 56*x
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