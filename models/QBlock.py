from models.MarioObject import MarioObject


class QBlock(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str) -> None:
        super().__init__(coordinates, image_path)
        self.property = None
