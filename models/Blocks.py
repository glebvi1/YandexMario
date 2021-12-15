from pygame import sprite, image


class Block(sprite.Sprite):
    def __init__(self, coordinate: tuple, image_path: str):
        sprite.Sprite.__init__(self)
        self.coordinate = coordinate
        self.image_path = image_path

        self.image = image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(coordinate[0], coordinate[1]))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, delta_time):
        pass
