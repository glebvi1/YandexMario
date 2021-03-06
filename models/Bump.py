from math import fabs

from pygame import sprite

from models import BUMP_MOVE, BUMP_MAX_LEN
from models.MarioObject import MarioObject
from models.QBlock import QBlock


class Bump(MarioObject):
    def __init__(self, coordinates: tuple, image_path: str, direction: int) -> None:
        """Создаем бомбу с направлением, при direction=0, бомба двигаться не будет
        :param coordinates: координаты бомбы
        :param image_path: путь к картинке бомбы
        :param direction: направление движения бомбы
        """
        super().__init__(coordinates, image_path)
        self.dir_x = BUMP_MOVE * direction

    def update(self, dt: int) -> bool:
        """Передвигаем бомбу
        :param dt: время в милисекундах
        """
        self.rect.x += MarioObject._direction_round(self.dir_x * dt / 100)
        if fabs(self.coordinate[0] - self.rect.x) >= BUMP_MAX_LEN:
            return False
        return True

    def __collide_with_enemies(self, enemies: list) -> bool:
        """Пересечение бомбы с врагами
        :param enemies: список врагов
        """
        for enemy in enemies:
            if sprite.collide_mask(self, enemy):
                enemies.remove(enemy)
                return True
        return False

    def __collide_with_blocks(self, blocks: list, enemies: list, bonus: list) -> bool:
        """Пересечение бомбы с блоками, в том числе и с Q-блоками
        :param blocks: список блоков
        :param enemies: список врагов
        :param bonus: список бонусов
        """
        for block in blocks:
            if sprite.collide_mask(self, block):
                if isinstance(block, QBlock):
                    block.get_action(blocks, enemies, bonus)
                return True
        return False

    def is_collide(self, blocks, enemies, bonus) -> bool:
        """Было ли пересечение бомбы с другими объектами
        :param blocks: список блоков
        :param enemies: список врагов
        :param bonus: список бонусов
        """
        return self.__collide_with_blocks(blocks, enemies, bonus) or self.__collide_with_enemies(enemies)
