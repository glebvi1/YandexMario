from models.MarioObject import MarioObject
from models.Bump import Bump
from models import STATE_CONTINUE, STATE_END, STATE_WIN, MARIO_SPEED,\
    MARIO_JUMP_POWER, GRAVITATION, MARIO_HEIGHT

from config import ANIMATED_RIGHT, ANIMATED_JUMP, ANIMATED_LEFT, ANIMATED_STATE, \
    ANIMATED_LJUMP, ANIMATED_RJUMP, BUMP_PATH
from pygame import sprite, image


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

        self.count_bumps = 3
        self.active_bump = None

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

        if self.active_bump is not None:
            if not self.active_bump.update(dt):
                self.active_bump = None
            elif self.active_bump.is_collide(window.blocks, window.enemies):
                self.active_bump = None

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

    def __throw_bump(self):
        if self.count_bumps > 0 and self.active_bump is None:
            self.count_bumps -= 1
            bumps_coords = (self.rect.x + 10, self.rect.y + MARIO_HEIGHT // 2)
            bump = Bump(bumps_coords, BUMP_PATH)
            self.active_bump = bump

    def __set_direction(self, vector: tuple) -> None:
        """Метод задает направление движения
        :param vector: кортеж с направлениями
        """
        right, left, up, throw = vector

        if up:
            if self.on_ground:
                self.direction_y = -MARIO_JUMP_POWER
            self.image = image.load(ANIMATED_JUMP).convert_alpha()

        if left:
            self.direction_x = -MARIO_SPEED
            if not up:
                self.image = image.load(ANIMATED_LEFT).convert_alpha()
            else:
                self.image = image.load(ANIMATED_LJUMP).convert_alpha()
        elif right:
            self.direction_x = MARIO_SPEED
            if not up:
                self.image = image.load(ANIMATED_RIGHT).convert_alpha()
            else:
                self.image = image.load(ANIMATED_RJUMP).convert_alpha()
        else:
            self.direction_x = 0
            if not up:
                self.image = image.load(ANIMATED_STATE).convert_alpha()

        if not self.on_ground:
            self.direction_y += GRAVITATION

        if throw:
            self.__throw_bump()

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

    def draw(self, screen, camera):
        """Отрисовываем спрайт
        :param screen: экран игры
        :param camera: камера
        """
        screen.blit(self.image, (self.rect.x - camera.state.x, self.rect.y - camera.state.y))
        if self.active_bump is not None:
            screen.blit(self.active_bump.image, (self.active_bump.rect.x - camera.state.x, self.active_bump.rect.y - camera.state.y))
