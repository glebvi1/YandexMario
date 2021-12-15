from pygame import sprite, image


class Hero(sprite.Sprite):
    def __init__(self, coordinate: tuple, image_path: str, life=3):
        sprite.Sprite.__init__(self)
        self.coordinate = coordinate
        self.life = life

        self.image_path = image_path
        self.image = image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(coordinate[0], coordinate[1]))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
