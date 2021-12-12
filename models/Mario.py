from models.Hero import Hero
from pygame import sprite

WIDTH = 22
HEIGHT = 30
MOVE_SPEED = 7
JUMP_SPEED = 100


class Mario(Hero):
    def __init__(self, coordinate: tuple, image_path: str):
        super().__init__(coordinate, image_path)
        self.on_ground = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, direction_x, direction_y):
        self.rect.x += MOVE_SPEED * direction_x
        if self.on_ground:
            self.rect.y -= JUMP_SPEED * direction_y
        if not self.on_ground:
            self.rect.y += 1

    def update(self, direction_x, direction_y, blocks):
        if direction_x != 0 and direction_y != 0:
            self.collide(0, direction_y, blocks)
            self.collide(direction_x, 0, blocks)
        else:
            self.collide(0, 0, blocks)

    def collide(self, direction_x, direction_y, blocks):
        current_on_ground = False
        for block in blocks:
            if sprite.collide_rect(self, block):
                is_bottom_collide = True

                if direction_x == 1 and self.on_ground:  # вправо
                    self.rect.right = block.rect.left
                    is_bottom_collide = False

                if direction_x == -1:  # влево
                    self.rect.left = block.rect.right
                    is_bottom_collide = False

                if direction_y == 1:  # вверх
                    self.rect.top = block.rect.bottom
                    is_bottom_collide = False

                # пересечение внизу
                if is_bottom_collide:  # вниз
                    current_on_ground = True
                    self.rect.bottom = block.rect.top

        self.on_ground = current_on_ground
        print(self.on_ground)
