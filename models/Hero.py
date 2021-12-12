from pygame import sprite, image


class Hero(sprite.Sprite):
    def __init__(self, coordinate: tuple, image_path: str):
        sprite.Sprite.__init__(self)
        self.start_coordinate = coordinate
        self.life = 3

        self.image_path = image_path
        self.image = image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(coordinate[0], coordinate[1]))
