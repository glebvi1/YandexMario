from models.MarioObject import MarioObject


class Teleport(MarioObject):
    def __init__(self, coordinate: tuple, image_path: str, go_coords):
        super().__init__(coordinate, image_path)
        self.go_coords = go_coords
