import random as rd
from typing import List

from config import BLOCKS_PATH, MOVE_FIRE_PATH, BUMP_PATH
from models.MarioObject import MarioObject
from models.MoveFire import MoveFire

ACTION = {
    1: "Block",
    2: "Enemy",
    3: "Bump"
}


class QBlock(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str) -> None:
        super().__init__(coordinates, image_path)
        self.action = ACTION[rd.randint(1, len(ACTION))]

    def get_action(self, blocks: List[MarioObject], enemies: List[MarioObject], bonus: List[MarioObject]):
        blocks.remove(self)
        if self.action == "Block":
            blocks.append(MarioObject(self.coordinate, BLOCKS_PATH))
        elif self.action == "Enemy":
            enemies.append(MoveFire(self.coordinate, MOVE_FIRE_PATH, direction=0))
        elif self.action == "Bump":
            from models.Bump import Bump
            bonus.append(Bump(self.coordinate, BUMP_PATH, direction=0))
