import random

import pygame
import pygame.mouse as pygmouse
import pygame.font as pygfont

import objects
from field import GameField
from objects import AIDev
from renderer import Renderer

window_size = (1280, 720)
window = pygame.display.set_mode(window_size)
running = True
pygfont.init()

counter1font = pygfont.Font("./assets/DSEG7.ttf", 32)

# game vars
gameField = GameField((10, 6))
render = Renderer(window, gameField, physObjSize=(50, 50))
physObjects = []
# codeblocks and maybe something more?
gameValues = {
    "codeblocks": 50
}
# cards
cards = [objects.AIDevCard(), None, None, None, None, None]
selectedCard = -1
prog_card_map = {
    1: AIDev
}
# card collision
collisionDelay = 60
lastCollision = int(collisionDelay)




def mouseInObj(obj: objects.PhysObj):
    mousepos = pygmouse.get_pos()
    if obj.x < mousepos[0] < obj.x + render.physsize[0]:
        if obj.y < mousepos[1] < obj.y + render.physsize[1]:
            return True
    return False


def doGameAction(x: int, y: int, res: objects.ObjectReturnData):
    global gameValues, gameField
    if res is None:
        return

    if res.action == "summon":
        pos_center = render.getCenterForCell(x, y)
        newobj = None
        if res.values[0] == "codeblock":
            newobj = objects.CodeBlock(
                pos_center[0] - (render.physsize[0] / 2) + random.randint(-10, 10),
                pos_center[1] - (render.physsize[1] / 2) + random.randint(-5, 5),
                res.values[1]
            )
        physObjects.append(newobj)
    elif res.action == "gain":
        if res.values[0] == "codeblock":
            gameValues["codeblocks"] += res.values[1]
    elif res.action == "plant":
        if res.values[0] == 1:
            if gameValues["codeblocks"] >= AIDev.cost:
                gameField.field[x][y] = AIDev()
                gameValues["codeblocks"] -= AIDev.cost


while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
    mousepos = pygmouse.get_pos()

    # gameplay loop goes here
    for x in range(len(gameField.field)):
        for y in range(len(gameField.field[0])):
            item = gameField.field[x][y]
            if item is not None:
                res = item.onGameTick()
                doGameAction(x, y, res)
            elif render.getBoundingBoxForCell(x, y).collidepoint(pygmouse.get_pos()):
                if pygmouse.get_pressed()[0] and selectedCard > -1:
                    doGameAction(
                        x, y, objects.ObjectReturnData(
                            "plant",
                            (cards[selectedCard].progid,)
                        )
                    )
                    selectedCard = -1

    for obj in physObjects:
        obj.onGameTick()
        if mouseInObj(obj):
            doGameAction(0, 0, obj.onMouseOver())
            physObjects.remove(obj)
    # card detection
    for i in range(len(cards)):
        if cards[i]:
            rect = pygame.Rect(
                150 + render.textman.cardsize[0] * i,
                10,
                render.textman.cardsize[0],
                render.textman.cardsize[1]
            )
            if rect.collidepoint(mousepos) and lastCollision > 120:
                lastCollision = 0
                if pygmouse.get_pressed()[0]:
                    selectedCard = i if selectedCard == -1 else -1
            lastCollision += 1 if lastCollision <= 120 else 0

    ## render loop goes here
    window.fill((0, 0, 0))
    # ui
    window.blit(
        counter1font.render(str(gameValues["codeblocks"]), True, (255, 255, 255)),
        (25, 10 + (render.textman.cardsize[1] / 2) - 16)
    )
    # cards
    for i in range(len(cards)):
        if cards[i]:
            render.renderCard(150 + render.textman.cardsize[0] * i, 10, cards[i].cardid)
    # selected card
    if selectedCard > -1:
        render.renderGameObjectFree(mousepos[0], mousepos[1], cards[selectedCard].progid)
    # render field objects
    for x in range(len(gameField.field)):
        for y in range(len(gameField.field[0])):
            if render.getBoundingBoxForCell(x, y).collidepoint(pygmouse.get_pos()):
                render.renderCell(x, y, color=(255, 0, 0))
            else:
                render.renderCell(x, y, color=(0, 255, 0))

            if gameField.field[x][y] is not None:
                render.renderGameObject(x, y, gameField.field[x][y].objid)
    # render phys objects
    for obj in physObjects:
        render.renderPhysObject(obj)

    pygame.display.flip()
