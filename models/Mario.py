from models import STATE_CONTINUE, STATE_END, STATE_WIN
from models.MarioObject import MarioObject
from pygame import sprite
from math import ceil, floor

WIDTH = 22
HEIGHT = 30
MOVE_SPEED = 20
JUMP_POWER = 50
GRAVITATION = 2.5


class Mario(MarioObject):
    def __init__(self, coordinate: tuple, image_path: str):
        super().__init__(coordinate, image_path)
        self.on_ground = False
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.direction_x = 0
        self.direction_y = 0

    def update(self, dt, vector, window) -> int:
        if self.collide_with_enemies(window.enemies):
            return STATE_END
        if sprite.collide_mask(self, window.princess):
            return STATE_WIN

        self.set_direction(vector)
        self.move(dt, window.blocks)
        return STATE_CONTINUE

    def move(self, dt, platforms):
        self.on_ground = False
        self.rect.y += Mario.direction_round(self.direction_y * dt / 100)
        self.collide_with_blocks(0, self.direction_y, platforms)

        self.rect.x += Mario.direction_round(self.direction_x * dt / 100)
        self.collide_with_blocks(self.direction_x, 0, platforms)

    def set_direction(self, vector):
        right, left, up = vector

        if up:
            if self.on_ground:  # прыгаем, только когда можем оттолкнуться от земли
                self.direction_y = -JUMP_POWER

        if left:
            self.direction_x = -MOVE_SPEED  # Лево = x- n

        if right:
            self.direction_x = MOVE_SPEED  # Право = x + n

        if not (left or right):
            self.direction_x = 0

        if not self.on_ground:
            self.direction_y += GRAVITATION

    def collide_with_blocks(self, control_x, control_y, platforms):
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

    def collide_with_enemies(self, enemies: list) -> bool:
        """True - если было пересечение с врагом, иначе - False
        :param enemies: списое врагов
        """
        for enemie in enemies:
            if sprite.collide_rect(self, enemie):
                return True
        return False

    @staticmethod
    def direction_round(direction):
        """Метод округляет направление до целого числа
        :param direction: направление
        """
        return ceil(direction) if direction > 0 else floor(direction)
