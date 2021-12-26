from pygame import sprite, image
from models.MarioObject import MarioObject


class Block(MarioObject):
    def __init__(self, coordinate: tuple, image_path: str):
        sprite.Sprite.__init__(self)
        self.coordinate = coordinate
        self.image_path = image_path

        self.image = image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(coordinate[0], coordinate[1]))
