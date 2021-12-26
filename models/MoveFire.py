from models.MarioObject import MarioObject
from math import fabs
from models import FIRE_MOVE


class MoveFire(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str,
                 max_len: int):
        super().__init__(coordinates, image_path)

        self.max_len = max_len
        self.dir_x = FIRE_MOVE

    def update(self, dt):
        self.rect.x += MarioObject._direction_round(self.dir_x * dt / 100)

        if fabs(self.coordinate[0] - self.rect.x) >= self.max_len:
            self.dir_x = -self.dir_x
