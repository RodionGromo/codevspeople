class GameField:
    def __init__(self, fieldSize: tuple):
        self.field = [[None] * fieldSize[1] for _ in range(fieldSize[0])]


