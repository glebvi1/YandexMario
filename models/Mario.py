from models.Hero import Hero
from pygame import sprite

WIDTH = 22
HEIGHT = 32
MOVE_SPEED = 7
JUMP_SPEED = 15


class Mario(Hero):
    def __init__(self, coordinate: tuple, image_path: str):
        super().__init__(coordinate, image_path)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, direction_x, direction_y):
        self.rect.x += MOVE_SPEED * direction_x
        self.rect.y += JUMP_SPEED * direction_y

    def update(self, direction_x, direction_y, blocks):
        self.collide(direction_x, direction_y, blocks)

    def collide(self, direction_x, direction_y, blocks):
        for block in blocks:
            if sprite.collide_rect(self, block):

                if direction_x == 1:  # вправо
                    self.rect.right = block.rect.left
                if direction_x == -1:  # влево
                    self.rect.left = block.rect.right
                if direction_y == -1:  # вверх
                    self.rect.top = block.rect.bottom
