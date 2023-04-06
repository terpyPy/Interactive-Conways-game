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
import os
import time
from boardStateDriver import boardState
from gameSettings import Settings
from deBugTiles import tileWindow
import sys
import pygame
import pygame.display
import pygame.event
import pygame.mouse
from tile import tileGroup
import pygame_textinput


class LightsOutGame:
    # over all class to manage the game
    def __init__(self, N: int) -> object:
        # init game and create screen game resource
        pygame.init()
        self.isDebugActivity = False
        # N is either NxN grid or *args is a list of modifiers
        self.N = N
        self.newLine = None
        # init the UI, N is passed to size the list comprehension,
        # was written to allow rebuilding the game in any NxN grid
        self.create_board_UI(buildNew= False)
        #
        self.menuKeys = self.settings.menuKeys
        self.pauseKeys = self.settings.pauseKeys
        self.option = 'new_rules'
        # init the UI, N is passed to size the list comprehension,
        # was written to allow rebuilding the game in any NxN grid
        # self.create_board_UI()
        # this library makes having user type box easy, not good
        resourcPath = os.path.join(
            os.environ.get("_MEIPASS2", os.path.abspath(".")), 'images\\freesansbold.ttf')
        self.textinput = pygame_textinput.TextInputVisualizer(
            font_object=pygame.font.Font(resourcPath, 20))

        # set the clock for pygame this will be used to synchronize
        # the game with the framerate of the display
        self.clock = pygame.time.Clock()
        self.clock.tick(self.settings.animation_FPS)

    def create_board_UI(self, buildNew= False):
        # this makes bsdrive
        """TODO: make all this functions dependent on this function take *args 
        this allows for proper board size creation in window & on the fly reshaping."""
        # make screen surface
        self.screen = pygame.display.set_mode(
            (800, 800))
        pygame.display.set_caption("lights out")
        self.settings = Settings(
            self.N,
            screen=(800, 800),
            isGlobal=False)

        # init the grid drawn over each tile
        self.board = tileGroup(self)
        print(self.board.tileArray[0][0].get_img_size())
        option1_cords = (0, 0)
        option2_cords = (0, self.N//2)
        option3_cords = (0, self.N//15)
        self.new_rules_button = self.board.make_Tile(option1_cords, 'new_rules', build_new=buildNew)
        self.FPS_option_button = self.board.make_Tile(option2_cords, 'FPS', build_new=buildNew)
        # passing self gives the Tile obj a current instance of the state
        self.driver = boardState(self)

        self.rulesText = self.board.make_Tile(option3_cords, 'rules', build_new=buildNew)
        self.FPS_option_button.set_msg(
            f'Option FPS:- currently={self.settings.animation_FPS}')
        self.rulesText.set_msg(f'current rule: {self.driver.rules}')
        # set option button color
        self.new_rules_button.set_color([250,250,250])
        self.FPS_option_button.set_color([250,250,250])
        # the draw vector is used to draw the grid over the tiles
        # x = list(range(0,5))*5
        # print(list(x), list(reversed(x)))
        self.draw_vec_i = list(range(0, self.N))*self.N
        # reverse the draw vector
        self.draw_vec_j = self.draw_vec_i.copy()[::-1]
        # reassign the draw vector i to row wise order
        self.draw_vec_i = [x for x in range(
            0, self.N) for y in range(0, self.N)]
        # hashmaps for the draw vector
        self.tileMap = map(self.board.drawTile,
                           self.draw_vec_i, self.draw_vec_j)

        x, y, img_size = self.board.getTextXY()
        self.texWincord1 = x-(img_size)
        self.texWincord2 = y+img_size

    @property
    def tileMap(self):
        """draw the tiles on the screen with the draw vecs"""
        return map(self.board.drawTile, 
                   self.draw_vec_i, 
                   self.draw_vec_j,
                   [False] * len(self.draw_vec_i),
                   [self.isDebugActivity] * len(self.draw_vec_i))

    @tileMap.setter
    def tileMap(self, value):
        self._tileMap = value

    def windPrompt(self):
        '''should use the logic applied in this function 
        to enter custom & random board sizes and shapes'''
        if self.textinput.value.isdigit():
            self.N = int(self.textinput.value)
            del self.board
            del self.driver
            del self.new_rules_button
            del self.settings
            # self.driver.resetDriver()
            self.create_board_UI(True)
        self.textinput.value = ''
        self.driver.mode = 'start'

    def _check_events(self):
        events = pygame.event.get()
        # lockout events if not an event used in the game
        if pygame.MOUSEBUTTONDOWN or pygame.KEYDOWN in events:
            self.textinput.update(events)
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #
                    x, y = event.pos
                    # soo im just lazy and this works fine, for future,
                    # just compare the len(lst-1) before returning it, try returning -1,-1 on error
                    # try:
                    i, j = self._get_button_click(x, y)
                    if i != None:
                        self.driver.boardLogic((i, j))
                        return

                if event.type == pygame.KEYDOWN:
                    # if key is pressed check its mapping to its options,
                    self._menu_Keys(event.key)
                    return

        # after events are checked, match them to the game logic
        if self.driver.mode == 'AI':
            cpuMove = self.driver.cpuPlay()
            self.driver.boardLogic(cpuMove)
            
        elif self.settings.mode == 'start':
            self.driver.boardLogic(-2)

    def _get_button_click(self, x, y):
        tile_view = self.board.tileArray
        # check if a menu button was clicked
        if self.new_rules_button.rect.collidepoint(x, y):
            self.option = 'new_rules'
            return (None, None)
        elif self.FPS_option_button.rect.collidepoint(x, y):
            self.option = 'fps_option'
            return (None, None)
        # check the board click.
        for i in range(self.N):
            for j in range(self.N):
                # find the location that the click was on a valid tile
                if tile_view[i][j].rect.collidepoint(x, y):
                    print(x, y, (i, j))
                    # return the correct tile location in the array
                    return (i, j)

        return (None, None)

    def _menu_Keys(self, eventKey: int):
        # check if a key is pressed and change the mode accordingly
        #
        # q to quit while running
        if eventKey == pygame.K_q:
            sys.exit()

        # check menu keys.
        if eventKey in self.menuKeys.keys():
            self.driver.mode = self.menuKeySwitcher(eventKey, self.driver.mode)
            if self.driver.getMode() != 'nGame':
                self.driver.clearBoard()
                # clear the cursor box for user input, cannot be done in draw function
                self.textinput.value = ''
                print(self.driver.mode)
                # return

        # control start screen ui events here.
        if self.driver.getMode() == 'start':
            # if key press return build new UI of its size.
            if eventKey == pygame.K_RETURN:
                self.windPrompt()
                # return

        # toggle's that can be read while running the game
        elif self.driver.getMode() in ['run', 'nGame', 'draw']:
            # if the game is running, then the board state can be frozen
            if eventKey in self.pauseKeys.keys():
                self.driver.isPause = self.pauseFunc(eventKey)

            # toggle colors on and off
            if eventKey == pygame.K_c:
                self.driver.isMulticolor = self.toggleColors()
                print(
                    f'Debug_option-is-Multicolor_:-{self.driver.isMulticolor}')
                # return

            # toggle debug mode on and off
            elif eventKey == pygame.K_d:
                self.isDebugActivity = not self.isDebugActivity
                print(f'Debug_option-node-ACTIVITY_:-{self.isDebugActivity}')
                # return

    def menuKeySwitcher(self, event, mode):
        # take the event key and return the correct menu option
        menuOption = self.menuKeys.get(event)
        if menuOption:
            return menuOption
        else:
            return mode

    def toggleColors(self):
        #
        # clear the cursor box for user input, cannot be done in draw function
        if self.driver.isMulticolor:
            return False
        else:
            return True

    def pauseFunc(self, event):
        # clear the cursor box for user input, cannot be done in draw function
        # pausePrompt = 'PAUSED:-- Change Rule\'s: 3 integers > 9.'
        if event == pygame.K_a:
            # self.new_rules_button.set_msg(pausePrompt)
            self.textinput.value = ''
            print(f'paused_simulation-KEYPRESS_a: {not self.driver.isPause}')
            return not self.driver.isPause

        # functionality for changing conway's game rules from pause state
        if event == pygame.K_RETURN:
            # unpack the flags used to change the rules, and unpause the game
            # bypass is -2 as the event as its not a plausible option from user
            BYPASS_EVENT, OFF_PAUSE = self.pauseKeys.get(event)

            # parse the user input and change the rules
            if ',' in self.textinput.value and self.option == 'new_rules':
                rulesFromUser = self.textinput.value.split(',')
                print(
                    f" current rule {self.driver.rules} changed to {rulesFromUser}")
                self.driver.boardLogic(BYPASS_EVENT, rulesFromUser)
                self.newLine = None
                print(f'paused_simulation-CHANGED_RULES: {OFF_PAUSE}')
                return OFF_PAUSE

            # parse the user input and change the FPS
            elif self.option == 'fps_option':
                self.settings.animation_FPS = int(self.textinput.value)
                print(f'paused_simulation-CHANGED_FPS: {OFF_PAUSE}')
                return OFF_PAUSE

            # invalid input from user display error message
            else:
                self.addedText = (f'invalid input: {self.textinput.value}')
                self.newLine = tileWindow(self,
                                          self.addedText,
                                          0,
                                          0)

                self.textinput.value = ''
                print(f'paused_simulation-INVALID_INPUT: {not OFF_PAUSE}')
                return not OFF_PAUSE

    def updateButton(self, button, isTxt=False, onlyTxt=False, clickable=False, msg=None):
        # update the button state
        button.blitme(isTxt, onlyTxt)
        if isTxt and msg:
            button.set_msg(msg)
        if clickable:
            self.screen.blit(self.textinput.surface,
                             (button.rect.x,
                              button.rect.y)
                             )

    def _update_screen(self):
        # redraw screen surface ea loop
        self.screen.fill(self.settings.bg_color)
        # use the tileMap to draw the tiles on the screen with the draw vecs
        list(self.tileMap)
        # print(f'update_screen-tileMap: {tileMap}')

        # draw text input if correct option,
        # this handles the text input for the user to change the grid size.
        if self.driver.getMode() == 'start':
            # args: [True,'enter NxN grid to make:',True]
            self.updateButton(self.new_rules_button,
                              isTxt=True,
                              onlyTxt=False,
                              clickable=True,
                              msg='enter NxN grid to make:')

        # handle the idle state of the game when paused.
        if self.driver.isPause:
            self.new_rules_button.blitme(debug=True, txtOnly=False)
            self.FPS_option_button.blitme(debug=True, txtOnly=False)
            # draw the text input for the user to change the rules.
            if self.option == 'new_rules':
                # new_rules_button, True, False, True,'PAUSED:-- Change Rule\'s: 3 integers > 9.'
                self.updateButton(self.new_rules_button,
                                  isTxt=True,
                                  onlyTxt=False,
                                  clickable=True,
                                  msg='Option Change Rule\'s:-- 3 integers > 9.')
                self.updateButton(self.rulesText,
                                  isTxt=True,
                                  onlyTxt=True,
                                  msg=f'Current Rule\'s: {self.driver.rules}')

            # draw the text input for the user to change the FPS.
            if self.option == 'fps_option':
                self.updateButton(self.FPS_option_button,
                                  isTxt=True,
                                  onlyTxt=False,
                                  clickable=True,
                                  msg=f'Option FPS:- currently={self.settings.animation_FPS}')

            # draw the text input for invalid input from user.
            if self.newLine:
                self.newLine.x = self.new_rules_button.rect.x
                self.newLine.y = self.new_rules_button.rect.y+30
                self.newLine.blitme(self.addedText)

            
        
        self.clock.tick(self.settings.animation_FPS)
        # make most recent drawn screen appear
        pygame.display.flip()

    def run_game(self, user_input=None):
        # this is the event loop for the UI,
        # 1) chose the play type
        # 2) check the events, ie button press on keyboard and the window
        # 3) draw the result of listening to the event or driver logic execution
        while True:
            # print(user_input)
            # 1
            self._check_events()
            # 2
            self._update_screen()
            # 3
            if self.driver.isWin:
                time.sleep(1.2)
                self.driver.clearBoard()
                self.driver.randomStart()
                self.driver.isWin = False


if __name__ == '__main__':
    # create a new game instance
    startNum = 75
    state = LightsOutGame(int(startNum))
    state.run_game()
