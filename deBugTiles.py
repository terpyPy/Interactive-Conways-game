import pygame

class tileWindow:
    def __init__(self, state,n,x,y):
        self.msg = n
        self.screen = state.screen
        self.x = x+5
        self.y = y+5
        self.font = pygame.font.Font('freesansbold.ttf', 11)
    def blitme(self,msg):
        
        self.text = self.font.render(str(msg-1), True, (250,0,0), (250,250,250))
        self.screen.blit(self.text, (self.x, self.y))