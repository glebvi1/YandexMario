from math import fabs

from models import FLY_DEATH_XMOVE, FLY_DEATH_MAX_LEN, FLY_DEATH_MAX_HEIGHT, FLY_DEATH_YMOVE
from models.MarioObject import MarioObject


class FlyDeath(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str) -> None:
        super().__init__(coordinates, image_path)
        self.dir_x = FLY_DEATH_XMOVE
        self.dir_y = FLY_DEATH_YMOVE

    def update(self, dt, blocks):
        self.rect.x += MarioObject._direction_round(self.dir_x * dt / 100)
        self.rect.y += MarioObject._direction_round(self.dir_y * dt / 100)

        if fabs(self.coordinate[0] - self.rect.x) >= FLY_DEATH_MAX_LEN:
            self.dir_x = -self.dir_x

        if fabs(self.coordinate[1] - self.rect.y) >= FLY_DEATH_MAX_HEIGHT:
            self.dir_y = -self.dir_y
