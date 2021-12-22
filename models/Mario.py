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

    def update(self, dt, vector, platforms):
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

        self.on_ground = False
        self.rect.y += Mario.direction_round(self.direction_y * dt / 100)
        self.collide(0, self.direction_y, platforms)

        self.rect.x += Mario.direction_round(self.direction_x * dt / 100)
        self.collide(self.direction_x, 0, platforms)
        return True

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.on_ground = True  # и становится на что-то твердое
                    self.direction_y = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.direction_y = 0  # и энергия прыжка пропадает

    @staticmethod
    def direction_round(direction):
        return ceil(direction) if direction > 0 else floor(direction)

"""
    def update(self, dt, vector, window):
        right, left, up = vector

        if up and self.on_ground:
            self.direction_y = -JUMP_SPEED

        if left:
            self.direction_x = -MOVE_SPEED

        if right:
            self.direction_x = MOVE_SPEED

        if not (left or right):
            self.direction_x = 0

        if not self.on_ground:
            self.direction_y += GRAVITATION

        self.on_ground = False
        self.y = self.direction_y * dt / 1000
        self.rect.y += self.y
        self.collide_with_blocks(0, self.direction_y, window.blocks)

        self.x = self.direction_x * dt / 1000
        self.rect.x += self.x
        self.collide_with_blocks(self.direction_x, 0, window.blocks)
        return True

    def collide_with_blocks(self, direction_x, direction_y, blocks):
        for block in blocks:
            if sprite.collide_rect(self, block):

                if direction_x > 0:  # вправо
                    self.rect.right = block.rect.left
                    self.x = self.rect.right

                if direction_x < 0:  # влево
                    self.rect.left = block.rect.right
                    self.x = self.rect.left

                if direction_y > 0:  # вверх
                    self.rect.bottom = block.rect.top
                    self.y = self.rect.bottom
                    self.on_ground = True
                    self.direction_y = 0

                if direction_y < 0:
                    self.rect.top = block.rect.bottom
                    self.y = self.rect.top
                    self.direction_y = 0

    def collide_with_enemies(self, enemies: list) -> bool:
        True - если было пересечение с врагом, иначе False
        :param enemies: списое врагов
        
        for enemie in enemies:
            if sprite.collide_rect(self, enemie):
                return True
        return False


    def move(self, direction_x, direction_y, blocks):
        is_jumping = self.can_jump and direction_y != 0
        if not self.on_ground and direction_y == 0:
            self.rect.y += GRAVITATION

        if is_jumping:
            self.rect.y -= JUMP_SPEED * direction_y
            self.can_jump = False

        if direction_x == 0 and direction_y == 0:
            self.collide_with_blocks(0, 0, blocks)
        else:
            self.collide_with_blocks(0, direction_y, blocks)
            self.rect.x += MOVE_SPEED * direction_x
            self.collide_with_blocks(direction_x, 0, blocks)
"""
