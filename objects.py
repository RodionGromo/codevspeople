import random


class ObjectReturnData:
    def __init__(self, action: str, values: tuple):
        self.action = action
        self.values = values


class CardObject:
    def __init__(self, name, cardid, progid):
        self.name = name
        self.cardid = cardid
        self.progid = progid

    def OnPlant(self) -> ObjectReturnData:
        return ObjectReturnData("plant", (self.name, -50))


class GameObject:
    def onGameTick(self) -> ObjectReturnData:
        pass


class PhysObj:
    objid = -1

    def __init__(self, x: int, y: int, vel: tuple):
        self.x = x
        self.y = y
        self.vel: list = list(vel)

    def onGameTick(self) -> ObjectReturnData:
        pass

    def onMouseover(self) -> ObjectReturnData:
        pass


class CodeBlock(PhysObj):
    name = "Code block"
    floatUpTimerMax = 800
    floatDownTimerMax = 1200
    objid = 0

    def __init__(self, x: int, y: int, value: int, vel: tuple = (0, 0)):
        super().__init__(x, y, vel)
        self.floatUpTimer = 0
        self.floatDownTimer = 0
        self.value = value
        self.xmove = random.uniform(-0.01, 0.01)

    def onGameTick(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        if self.floatUpTimer < self.floatUpTimerMax:
            self.floatUpTimer += 1
            self.vel[1] = -0.02
            self.vel[0] = self.xmove
        elif self.floatDownTimer < self.floatDownTimerMax:
            self.floatDownTimer += 1
            self.vel[1] = +0.03
        else:
            self.vel = [0, 0]

    def onMouseOver(self) -> ObjectReturnData:
        return ObjectReturnData("gain", ("codeblock", self.value))


class AIDev(GameObject):
    objid = 1
    name = "AI Developer"
    blockgen_counter_delay = 2000
    cost = 50

    def __init__(self):
        super()
        self.blockgen_counter = self.blockgen_counter_delay

    def onGameTick(self) -> ObjectReturnData:
        if self.blockgen_counter > 1:
            self.blockgen_counter -= 1
        else:
            self.blockgen_counter += self.blockgen_counter_delay
            return ObjectReturnData("summon", ("codeblock", 25))


class AIDevCard(CardObject):
    def __init__(self):
        super().__init__("AI Dev", 0, 1)
