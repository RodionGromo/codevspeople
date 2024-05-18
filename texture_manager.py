import os.path

import pygame.transform as pygtransform
import pygame.image as pygimage


class TextureManager:
    def __init__(self, cellSize: tuple, physSize: tuple):
        self.ready = False
        self.textures = {}
        self.cellsize = cellSize
        self.physsize = physSize
        self.cardsize = (cellSize[0], cellSize[1]*2)
        self.__load()
        self.__bake()

    def __load(self, path="./assets/textures", recursive=False) -> dict:
        final = {}
        for file in os.listdir(path):
            if file[-4:] == ".png":
                final[file[:-4]] = pygimage.load(path + "/" + file)
            else:
                final[file] = self.__load(path + "/" + file, recursive=True)
        if not recursive:
            self.textures = final
        return final

    def __bake(self):
        for key, img in self.textures["gameobj"].items():
            self.textures["gameobj"][key] = pygtransform.scale(img, self.cellsize)
        for key, img in self.textures["physobj"].items():
            self.textures["physobj"][key] = pygtransform.scale(img, self.physsize)
        for key, img in self.textures["cards"].items():
            self.textures["cards"][key] = pygtransform.scale(img, self.cardsize)

    def getPhysTexture(self, name: str):
        try:
            return self.textures["physobj"][name]
        except KeyError:
            return None

    def getGameTexture(self, name: str):
        try:
            return self.textures["gameobj"][name]
        except KeyError:
            return None

    def getCardTexture(self, name: str):
        try:
            return self.textures["cards"][name]
        except KeyError:
            return None
