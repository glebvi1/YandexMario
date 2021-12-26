from models import STATE_CONTINUE, STATE_END, STATE_WIN
from models.MarioObject import MarioObject
from pygame import sprite
from models import MARIO_SPEED, MARIO_JUMP_POWER, GRAVITATION


class Mario(MarioObject):
    def __init__(self, coordinate: tuple, image_path: str) -> None:
        """Главный персонаж - Марио
        :param coordinate: начальные координаты
        :param image_path: путь к картинке
        """
        super().__init__(coordinate, image_path)
        self.on_ground = False
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.direction_x = 0
        self.direction_y = 0

    def update(self, dt: int, vector: tuple, window) -> int:
        """Метод определяет состояние игры
        :param dt: время в милисекундах
        :param vector: кортеж с направлениями
        :param window: главное окно
        """
        if self.__collide_with_enemies(window.enemies):
            return STATE_END
        if sprite.collide_mask(self, window.princess):
            return STATE_WIN

        self.__set_direction(vector)
        self.__move(dt, window.blocks)
        return STATE_CONTINUE

    def __move(self, dt: int, platforms: list) -> None:
        """Метод передвигает Марио
        :param dt: время в милисекундах
        :param platforms: лист с блоками
        """
        self.on_ground = False
        self.rect.y += MarioObject._direction_round(self.direction_y * dt / 100)
        self.__collide_with_blocks(0, self.direction_y, platforms)

        self.rect.x += MarioObject._direction_round(self.direction_x * dt / 100)
        self.__collide_with_blocks(self.direction_x, 0, platforms)

    def __set_direction(self, vector: tuple) -> None:
        """Метод задает направление движения
        :param vector: кортеж с направлениями
        :return:
        """
        right, left, up = vector

        if up and self.on_ground:
            self.direction_y = -MARIO_JUMP_POWER

        if left:
            self.direction_x = -MARIO_SPEED

        if right:
            self.direction_x = MARIO_SPEED

        if not (left or right):
            self.direction_x = 0

        if not self.on_ground:
            self.direction_y += GRAVITATION

    def __collide_with_blocks(self, control_x: float, control_y: float, platforms: list) -> None:
        """Определяем столкновения с блоками
        :param control_x: направление по x
        :param platforms: лист с блоками
        :param control_y: направление по y
        :return:
        """
        for p in platforms:
            if sprite.collide_rect(self, p):

                if control_x > 0:  # вправо
                    self.rect.right = p.rect.left

                if control_x < 0:  # влево
                    self.rect.left = p.rect.right

                if control_y > 0:  # вниз
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.direction_y = 0

                if control_y < 0:  # вверх
                    self.rect.top = p.rect.bottom
                    self.direction_y = 0

    def __collide_with_enemies(self, enemies: list) -> bool:
        """True - если было пересечение с врагом, иначе - False
        :param enemies: список врагов
        """
        for enemie in enemies:
            if sprite.collide_rect(self, enemie):
                return True
        return False
