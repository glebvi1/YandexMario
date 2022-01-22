from models.MarioObject import MarioObject, BaseMarioObject


class BlockTeleport(BaseMarioObject):
    def __init__(self, x, y, goX,goY):
        super().__init__(self, x, y)
        self.goX = goX # координаты назначения перемещения
        self.goY = goY # координаты назначения перемещения