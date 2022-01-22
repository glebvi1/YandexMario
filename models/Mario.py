import time
from typing import Tuple, List

from pygame import sprite, image
from pygame.mixer import Sound

from config import BUMP_PATH, BUMBS_SOUND_PATH, STATE_CONTINUE, STATE_END, STATE_WIN, START_SOUND_PATH
from dao.db_mario_handler import save_game, get_level_number_by_win
from models import MARIO_SPEED, MARIO_JUMP_POWER, GRAVITATION, MARIO_HEIGHT, BUMP_WIDTH, ANIMATED_RIGHT, \
    ANIMATED_JUMP, ANIMATED_LEFT, ANIMATED_STATE, ANIMATED_LJUMP, ANIMATED_RJUMP
from models.Bump import Bump
from models.MarioObject import MarioObject
from models.Teleport import Teleport


class Mario(MarioObject):
    def __init__(self, coordinate: Tuple[int, int], image_path: str) -> None:
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

        self.count_bumps = 5
        self.count_money = 0
        self.active_bump = None
        self.last_throw = 100

        self.start_time = time.perf_counter()

        Sound(START_SOUND_PATH).play()

    def draw(self, screen, camera) -> None:
        """Отрисовываем спрайт
        :param screen: экран игры
        :param camera: камера
        """
        screen.blit(self.image, (self.rect.x - camera.state.x, self.rect.y - camera.state.y))
        if self.active_bump is not None:
            screen.blit(self.active_bump.image,
                        (self.active_bump.rect.x - camera.state.x, self.active_bump.rect.y - camera.state.y))

    def update(self, dt: int, vector: Tuple[bool, bool, bool, bool], window) -> int:
        """Метод определяет состояние игры
        :param dt: время в милисекундах
        :param vector: кортеж с направлениями
        :param window: главное окно
        """
        if self.__collide_with_enemies(window.enemies):
            self.__save_lose_game(window.level_number)
            return STATE_END
        if sprite.collide_mask(self, window.princess):
            save_game(True, self.get_current_time(), window.level_number, self.count_money)
            return STATE_WIN

        if self.active_bump is not None:
            if not self.active_bump.update(dt):
                self.active_bump = None

            elif self.active_bump.is_collide(window.blocks, window.enemies, window.bonus):
                self.active_bump = None

        self.__collide_with_bonus(window.bonus)
        self.__set_direction(vector)
        self.__move(dt, window.blocks)
        return STATE_CONTINUE

    def __move(self, dt: int, platforms: List[MarioObject]) -> None:
        """Метод передвигает Марио
        :param dt: время в милисекундах
        :param platforms: лист с блоками
        """
        self.was_collide = False
        self.on_ground = False
        self.rect.y += MarioObject._direction_round(self.direction_y * dt / 100)
        self.__collide_with_blocks(0, self.direction_y, platforms)

        self.rect.x += MarioObject._direction_round(self.direction_x * dt / 100)
        self.__collide_with_blocks(self.direction_x, 0, platforms)

    def __throw_bump(self, left: bool) -> None:
        """Марио бросает шишку
        :param left: двигается ли герой на лево
        """
        if self.count_bumps > 0 and self.active_bump is None and time.time() - self.last_throw > 0.5:
            direction = -1 if left else 1
            bumps_coords = (self.rect.x + BUMP_WIDTH, self.rect.y + MARIO_HEIGHT // 2)
            bump = Bump(bumps_coords, BUMP_PATH, direction)

            self.count_bumps -= 1
            self.active_bump = bump
            self.last_throw = time.time()
            Sound(BUMBS_SOUND_PATH).play()

    def __set_direction(self, vector: Tuple[bool, bool, bool, bool]) -> None:
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

        if throw and not self.was_collide:
            self.__throw_bump(left)

    def __collide_with_blocks(self, control_x: float, control_y: float,
                              platforms: List[MarioObject]) -> None:
        """Определяем столкновения с блоками
        :param control_x: направление по x
        :param platforms: лист с блоками
        :param control_y: направление по y
        """
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, Teleport):
                    self.__teleporting(p)

                if control_x > 0:  # вправо
                    self.rect.right = p.rect.left
                    self.was_collide = True

                if control_x < 0:  # влево
                    self.rect.left = p.rect.right
                    self.was_collide = True

                if control_y > 0:  # вниз
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.direction_y = 0

                if control_y < 0:  # вверх
                    self.rect.top = p.rect.bottom
                    self.direction_y = 0

    def __collide_with_enemies(self, enemies: List[MarioObject]) -> bool:
        """True - если было пересечение с врагом, иначе - False
        :param enemies: список врагов
        """
        for enemy in enemies:
            if sprite.collide_rect(self, enemy):
                return True
        return False

    def __collide_with_bonus(self, bonus: List[MarioObject]):
        for bon in bonus.copy():
            if sprite.collide_rect(self, bon):
                if isinstance(bon, Bump):
                    self.count_bumps += 2
                else:
                    self.count_money += 1

                bonus.remove(bon)

        return False

    def __save_lose_game(self, level_number) -> None:
        """Сохранение проигранного уровня в БД
        :param level_number: номер уровня
        """
        win_games = get_level_number_by_win(is_win=True)

        for level in win_games:
            if level[0] == level_number:
                return
        save_game(False, self.get_current_time(), level_number, self.count_money)

    def __teleporting(self, teleport):
        self.rect.x, self.rect.y = teleport.go_coords

    def get_current_time(self) -> str:
        """Время, проведенное в игре"""
        return Mario.__get_str_time(time.perf_counter() - self.start_time)
    @staticmethod
    def __get_str_time(game_time) -> str:
        """Перевод времени в строку"""
        minutes = int(game_time // 60)
        if minutes < 10:
            minutes = f"0{minutes}"
        seconds = int(game_time % 60)
        if seconds < 10:
            seconds = f"0{seconds}"
        return f"{minutes}:{seconds}"
