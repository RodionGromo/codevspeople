from typing import Union
import pygame
import pygame.draw as pygdraw

from field import GameField
from objects import PhysObj, CardObject
from texture_manager import TextureManager


def renderRect(window, x: int, y: int, w: int, h: int, color: tuple, outline_width: int = 1):
    rect = pygame.Rect(x, y, w, h)
    pygdraw.rect(window, color, rect, width=outline_width)


def renderImage(window, x: int, y: int, image: pygame.Surface):
    pass


class Renderer:
    def __init__(self, window: pygame.Surface, field: GameField, physObjSize: tuple):
        self.window = window
        # size for any physics object
        self.physsize = physObjSize
        # calc boundaries for cells
        self.cellBounds = pygame.Rect(0, 0, 0, 0)
        self.cellDimensions = pygame.Rect(0, 0, 0, 0)
        self.__calcCellSize(field)
        # setup textures
        self.textman = TextureManager((self.cellDimensions.w, self.cellDimensions.h), self.physsize)
        self.object_img_map = {
            0: {"img": self.textman.getPhysTexture("codeblock"), "color": (255, 255, 0)},
            1: {"img": self.textman.getGameTexture("aidev"), "color": (255, 255, 0)},
            2: {"img": None, "color": (255, 255, 0)}
        }
        self.card_img_map = {
            0: {"img": self.textman.getCardTexture("aidev"), "color": (0, 0, 255)}
        }

    def renderCard(self, x: int, y: int, card_id: int):
        self.window.blit(self.card_img_map[card_id]["img"], (x, y))

    def renderCell(self, x: int, y: int, color: tuple):
        bb = self.getBoundingBoxForCell(x, y)
        renderRect(self.window, bb.x, bb.y, bb.w, bb.h, color=color)

    def renderGameObjectFree(self, x, y, obj_id):
        img: pygame.Surface = self.object_img_map[obj_id]["img"]
        self.window.blit(
            img, (
                x - (img.get_size()[0] / 2),
                y - (img.get_size()[1] / 2)
            ))
    def getBoundingBoxForCell(self, x, y):
        return pygame.Rect(
            self.cellBounds.x + (self.cellDimensions.w * x),
            self.cellBounds.y + (self.cellDimensions.h * y),
            self.cellDimensions.w,
            self.cellDimensions.h
        )

    def getCenterForCell(self, x, y) -> tuple:
        return (
            (self.cellBounds.x + (self.cellDimensions.w * x)) + (self.cellDimensions.w // 2),
            (self.cellBounds.y + (self.cellDimensions.h * y)) + (self.cellDimensions.h // 2)
        )

    def __calcCellSize(self, field: GameField):
        windowSize = self.window.get_size()
        self.cellBounds = pygame.Rect(
            perc(windowSize[0], 6, True),  # left bound
            perc(windowSize[1], 25, True),  # top bound
            windowSize[0] - perc(windowSize[0], 5, True),  # right bound
            windowSize[1] - perc(windowSize[1], 5, True)  # bottom bound
        )
        self.cellDimensions = pygame.Rect(
            self.cellBounds.x,
            self.cellBounds.y,
            (self.cellBounds.w - self.cellBounds.x) / len(field.field),
            (self.cellBounds.h - self.cellBounds.y) / len(field.field[0])
        )

    def renderGameObject(self, x, y, obj_id: int):
        bb = self.getBoundingBoxForCell(x, y)
        img: pygame.Surface = self.object_img_map[obj_id]["img"]
        self.window.blit(img, (bb.x, bb.y))

    def renderPhysObject(self, obj: PhysObj):
        img: pygame.Surface = self.object_img_map[obj.objid]["img"]
        self.window.blit(
            img, (
                obj.x + (self.physsize[0] / 2) - (img.get_size()[0] / 2),
                obj.y + (self.physsize[1] / 2) - (img.get_size()[1] / 2)
            ))


def perc(x: int, y: int, coerceToInt: bool = False) -> (Union[float, int]):
    """
    Takes a percentage (0-100) from value\n
    :param x: value
    :param y: percentage
    :param coerceToInt: round the number
    :return: percentage of value
    """
    return int((x / 100) * y) if coerceToInt else ((x / 100) * y)
