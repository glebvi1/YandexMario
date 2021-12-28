from models.MarioObject import MarioObject
from models import BUMP_MOVE, BUMP_MAX_LEN
from pygame import sprite
from math import fabs


class Bump(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str, direction: int):
        super().__init__(coordinates, image_path)
        self.dir_x = BUMP_MOVE * direction

    def update(self, dt):
        self.rect.x += MarioObject._direction_round(self.dir_x * dt / 100)
        if fabs(self.coordinate[0] - self.rect.x) >= BUMP_MAX_LEN:
            return False
        return True

    def __collide_with_blocks(self, blocks) -> bool:
        for block in blocks:
            if sprite.collide_mask(self, block):
                return True
        return False

    def __collide_with_enemies(self, enemies: list):
        for enemy in enemies:
            if sprite.collide_mask(self, enemy):
                enemies.remove(enemy)
                return True
        return False

    def is_collide(self, blocks, enemies):
        return self.__collide_with_blocks(blocks) or self.__collide_with_enemies(enemies)
