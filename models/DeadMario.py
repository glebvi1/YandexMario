from math import fabs

from pygame.mixer import Sound

from config import DIE_SOUND_PATH
from models import GRAVITATION, DEAD_MARIO_LEN
from models.Mario import Mario
from models.MarioObject import MarioObject


class DeadMario(MarioObject):
    def __init__(self, mario: Mario, image_path: str):
        coords = (mario.rect.x, mario.rect.y)
        super().__init__(coords, image_path)

        Sound(DIE_SOUND_PATH).play()

    def update(self) -> bool:
        self.rect.y += 3 * GRAVITATION

        if fabs(self.coordinate[1] - self.rect.y) >= DEAD_MARIO_LEN:
            return False
        return True
