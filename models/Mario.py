from models.MarioObject import MarioObject
from pygame import sprite

WIDTH = 22
HEIGHT = 30
MOVE_SPEED = 5
JUMP_SPEED = 100
GRAVITATION = 2.5


class Mario(MarioObject):
    def __init__(self, coordinate: tuple, image_path: str):
        super().__init__(coordinate, image_path)
        self.on_ground = False
        self.can_jump = False

    def update(self, direction_x, direction_y, blocks, enemies):
        if self.collide_with_enemies(enemies):
            return False

        self.move(direction_x, direction_y, blocks)
        return True

    def move(self, direction_x, direction_y, blocks):
        is_jumping = self.can_jump and direction_y != 0
        if not self.on_ground and direction_y == 0:
            self.rect.y += GRAVITATION

        if is_jumping:
            self.rect.y -= JUMP_SPEED * direction_y
            self.can_jump = False

        if direction_x == 0 and direction_y == 0:
            self.collide_with_blocks(0, 0, blocks)
        else:
            self.collide_with_blocks(0, direction_y, blocks)
            self.rect.x += MOVE_SPEED * direction_x
            self.collide_with_blocks(direction_x, 0, blocks)

    def collide_with_blocks(self, direction_x, direction_y, blocks):
        current_on_ground = False
        for block in blocks:
            if sprite.collide_rect(self, block):
                is_bottom_collide = True

                if direction_x == 1:  # вправо
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
                    self.can_jump = True

        self.on_ground = current_on_ground

    def collide_with_enemies(self, enemies: list) -> bool:
        """True - если было пересечение с врагом, иначе False
        :param enemies: списое врагов
        """
        for enemie in enemies:
            if sprite.collide_rect(self, enemie):
                return True
        return False
