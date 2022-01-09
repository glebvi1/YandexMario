from math import fabs

from models import FIRE_MOVE, FIRE_MAX_LEN
from models.MarioObject import MarioObject


class MoveFire(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str) -> None:
        super().__init__(coordinates, image_path)
        self.dir_x = FIRE_MOVE

    def update(self, dt, blocks):
        self.rect.x += MarioObject._direction_round(self.dir_x * dt / 100)

        if fabs(self.coordinate[0] - self.rect.x) >= FIRE_MAX_LEN:
            self.dir_x = -self.dir_x
