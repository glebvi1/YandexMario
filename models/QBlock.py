import random as rd
from typing import List

from config import BLOCKS_PATH, FIRE_PATH
from models import FIRE_MAX_LEN
from models.MarioObject import MarioObject
from models.MoveFire import MoveFire

ACTION = {
    1: "Block",
    2: "Enemy",
    3: "Money"
}


class QBlock(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str) -> None:
        super().__init__(coordinates, image_path)
        self.action = ACTION[rd.randint(1, len(ACTION))]

    def get_action(self, blocks: List[MarioObject], enemies: List[MarioObject]):
        print("get_action")
        blocks.remove(self)
        if self.action == "Block":
            blocks.append(MarioObject(self.coordinate, BLOCKS_PATH))
        elif self.action == "Enemy":
            enemies.append(MoveFire(self.coordinate, FIRE_PATH, FIRE_MAX_LEN))
        elif self.action == "Money":
            pass
