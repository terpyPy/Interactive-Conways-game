#!/usr/bin/python3
#  Version:     1.2 (Date: 6/24/2022)
#  Author:      Cameron Kerley (terpyPY: https://github.com/terpyPy/Interactive-Conways-game)
#  Date:        6 June 2022
#  License:     MIT License
#
#  description: This is the main file for what makes up the the full tile entity.
#               Manages the tile entity's and grid entity's as a group/collection in tileGroup class.
# ----------------------------------------------------------------------------------------------------------------------
#  Disclosure:  This code is public domain. You can use it in any way you want.
#               However, i am scanning github repos for this code that does not include credit to me.
#               I have left some patterns in the naming convention and access methods
#               in this project making copy/pasted stolen code easy to parse and find.
#
# in pygame the origin is (0,0) at the top lft of the screen.
# cords > 0 for col->right col,row
#   0___> +col and <= 1200
#   |
#   v +row and <= 800
import json
import os
import pygame
import pygame.display
from deBugTiles import tileWindow
from grid import Grid


class Tile(Grid):

    def __init__(self, screen: pygame.display, rect=[], cords=[], settings={}, noScale=False, noPad=False, img=None, isJSON=False, data={}):
        """_summary_

        Args:
            screen (pygame.display): pygame surface to draw the obj.
            rect (pygame.rect): _description_
            cords (tuple): _description_
            settings (Settings): _description_
            noScale (bool, optional): _description_. Defaults to False.
            noPad (bool, optional): _description_. Defaults to False.
            img (str, optional): image to use for init. Defaults to None.
        """
        # init the tile and set its position
        self.imgPath = 'images\\tile.bmp'
        # super().__init__(screen, rect, cords, settings, noPad=noPad)
        # init the tile's image based on if it is a json file or not.
        if isJSON is False:
            super().__init__(screen, rect, cords, settings, noPad=noPad)
            self._create_init(cords, settings, noScale, img)
        else:
            print('is json')
            super().__init__(screen, data["rect"], data["cords"], settings, noPad=data["noPad"])
            self.init_from_Json(data, defSize=self.DEFAULT_SIZE)
            
        
        
    def init_from_Json(self, data, **kwargs):
        self.imgPath = data['path']
        self.img = pygame.image.load(self.imgPath)
        self.h, self.w = data['size']
        if not data['noScale']:
            self.img = pygame.transform.scale(self.img, (int(self.w), int(self.h)))
        else:
            self.img = pygame.transform.scale(self.img, kwargs['defSize'])
        # get the image rect from the image. also found in the json file if needed.
        self.rect = self.img.get_rect()
        self.setPad(data['cords'])
        self.Color = data['color']
        self.isEffected = data['isEffected']
        self.textWindow = tileWindow(
            self, self.isEffected, self.rect.x, self.rect.y)
        if data['noScale']:
            self.rect.y += 20
            self.rect.x += 2
        # make default msg the element name from json file.
        self.msg = data['element']
        
    def _create_init(self, cords, settings, noScale, img):
        if img is not None:
            self.imgPath = img
            resourcPath = os.path.join(
                os.environ.get("_MEIPASS2", os.path.abspath(".")), self.imgPath)
        else:
            resourcPath = os.path.join(
                os.environ.get("_MEIPASS2", os.path.abspath(".")), self.imgPath)

        # init image sizes & padding inherited from from grid.
        if noScale is False:
            self.img = pygame.image.load(resourcPath)
            
            self.h = (
                (settings.screen_height-self.DEFAULT_SIZE[0])//(settings.N))
            
            self.w = (
                ((settings.screen_height-self.DEFAULT_SIZE[0])-5)//(settings.N))
            self.img = pygame.transform.scale(self.img,
                                              (int(self.w), int(self.h)))
        else:
            self.img = pygame.image.load(resourcPath)
        # get the image rect
        self.rect = self.img.get_rect()
        # set the tile's x position with the cords provided.
        self.setPad(cords)
        # this is default rgb color of the tile. it is white by default.
        self.Color = settings.offColor
        # set node activity counter to .
        self.isEffected = 1
        self.textWindow = tileWindow(
            self, self.isEffected, self.rect.x, self.rect.y)
        if noScale:
            self.rect.y += 20
            self.rect.x += 2
        self.msg = 'default'
        
    def get_color(self):
        return self.Color

    def set_color(self, color):
        self.Color = color

    def set_msg(self, msg):
        self.msg = msg
        self.textWindow.set_font_size(int(self.textWindow.fontSize))

    def set_text_cords(self, x, y):
        self.textWindow.set_cords(x, y)

    def change_img(self, img):
        # change the image of the tile from file.
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()

    def usePixelArr(self, pixelArr, degree=90):
        # use the pixel array to change the image displayed on the tile. (read from memory NOT from file)
        self.img = pygame.surfarray.make_surface(pixelArr)
        self.img = pygame.transform.rotate(self.img, degree)
        self.img = pygame.transform.flip(self.img, False, True)

    def blitme(self, debug=False, txtOnly=False):
        # draw the obj at its current location, used for lights_out game.
        self.img.fill(self.Color)
        if debug and txtOnly is False:
            self.screen.blit(self.img, (self.rect.x, self.rect.y))
            self.textWindow.blitme(self.msg)
        elif txtOnly:
            self.textWindow.blitme(self.msg)
        else:
            self.screen.blit(self.img, (self.rect.x, self.rect.y))

    def blitme_pixel_array(self):
        # draw the obj at its current location, used for pixel array representation of an image.
        self.screen.blit(self.img, (self.rect.x, self.rect.y))
        self.textWindow.blitme(self.msg)


class tileGroup:
    def __init__(self, state, *args) -> None:
        # initialize the flags object with the flags passed in

        self.screen = state.screen
        self.screen_rect = state.screen.get_rect()
        self.N = state.N
        self.settings = state.settings
        # creates both the tile and grid entity groups, which can be modified together,
        # by the flags passed into the constructor
        self.tileArray = []
        self.gridArray = []
        self._make_entity_group()

    def _make_entity_group(self, *args) -> None:
        # *args is not currently used, but is there to allow for future expansion
        # create the tile and grid entity groups

        for i in range(self.N):
            self.tileArray.append([])
            self.gridArray.append([])
            for j in range(self.N):
                self.tileArray[i].append(
                    Tile(self.screen, self.screen_rect, (i, j), self.settings))
                self.gridArray[i].append(
                    Grid(self.screen, self.screen_rect, (i, j), self.settings))

    def getColors(self):
        # get the colors of the tiles in the tile group
        return list(map(lambda x: list(map(lambda y: y.get_color(), x)), self.tileArray))

    def setColors(self, colors):
        # set the colors of the tiles in the tile group
        return list(
            map(lambda x:
                list(
                    map(
                        lambda y: self.tileArray[x][y].set_color(colors[x][y]),
                        range(self.N)
                    )
                ),
                range(self.N)
                )
        )

    def getTextXY(self):
        x, y = [self.tileArray[0][self.N-1].rect.x,
                self.tileArray[0][self.N-1].rect.y]
        return x, y, self.tileArray[0][0].get_img_size()

    def make_Tile(self, cords, name='default', build_new=False):
        # check if there is a tile.json file, if not create one. if there is, load it instead.
        if (os.path.isfile(f'{name}.json')) and (build_new is False):
            # load the json file
            fp = open(f'{name}.json', 'r')
            data = json.load(fp)
            fp.close()
            # create the tile
            tile = Tile(self.screen, 
                        isJSON=True, 
                        data = data, 
                        settings=self.settings)
            
        else:
            tile = Tile(self.screen,
                        rect=self.screen_rect, 
                        cords=cords, 
                        settings=self.settings, 
                        noScale=True, 
                        noPad=True,)
            
            self._save_tile_json(element=name, 
                                cords=cords,
                                size=(tile.w, tile.h),
                                screenRect=list(self.screen_rect),
                                rect=list(tile.rect),
                                noScale=True, 
                                noPad=True,
                                path=tile.imgPath,
                                color=tile.Color,
                                isEffected=tile.isEffected)
        return tile

    def drawTile(self, i, j, txt=False, showGrid=False):
        self.tileArray[i][j].blitme(txt)
        if showGrid:
            self.gridArray[i][j].blitme()
        # self.gridArray[i][j].blitme()
        return self.tileArray[i][j].isEffected

    def _save_tile_json(self, **struc):
        """_summary_:
        save the tile structure to a json file.

        args:
            struc{key: value}: the structure of the tile to be saved. this is a dictionary,
            where key is a variable name and value is the value of that variable.
        """
        # write the json to the file
        fp = open(f'{struc["element"]}.json', 'w')
        json.dump(struc, fp)
        fp.close()