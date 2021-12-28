from models.MarioObject import MarioObject


class Bump(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str):
        super().__init__(coordinates, image_path)


