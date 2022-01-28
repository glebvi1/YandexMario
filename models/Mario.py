import time
from typing import Tuple, List

from pygame import sprite, image, Surface
from pygame.mixer import Sound

from config import BUMP_PATH, BUMBS_SOUND_PATH, STATE_CONTINUE, STATE_END, STATE_WIN, START_SOUND_PATH
from config.Camera import Camera
from dao.db_level_handler import save_game
from models import MARIO_SPEED, MARIO_JUMP_POWER, GRAVITATION, MARIO_HEIGHT, MARIO_WIDTH, BUMP_WIDTH, \
    ANIMATED_JUMP, ANIMATED_STATE, ANIMATED_LJUMP, ANIMATED_RJUMP, ANIMATED_LEFT, ANIMATED_RIGHT, \
    ANIMATED_LEFT2, ANIMATED_RIGHT2
from models.Bump import Bump
from models.MarioObject import MarioObject
from models.Teleport import Teleport

last_gid = 0


class Mario(MarioObject):
    def __init__(self, coordinate: Tuple[int, int], image_path: str, count_lives=3) -> None:
        """Главный персонаж - Марио
        :param coordinate: начальные координаты
        :param image_path: путь к картинке
        """
        super().__init__(coordinate, image_path)
        self.images = [image.load(path).convert_alpha() for path in
                       [ANIMATED_LEFT, ANIMATED_LEFT2, ANIMATED_RIGHT, ANIMATED_RIGHT2, ANIMATED_RJUMP,
                       ANIMATED_LJUMP, ANIMATED_JUMP, ANIMATED_STATE]]

        self.on_ground = False
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.direction_x = 0
        self.direction_y = 0

        self.count_bumps = 5
        self.count_lives = count_lives
        self.count_money = 0
        self.active_bump = None

        self.last_throw = 100
        self.last_die = 100

        self.frame = 0
        self.anim_v = 1

        self.start_time = time.perf_counter()
        self.is_saving = False

        Sound(START_SOUND_PATH).play()

    def draw(self, screen: Surface, camera: Camera) -> None:
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
        if time.time() - self.last_die < 1:
            return STATE_CONTINUE

        if self.__collide_with_enemies(window.enemies):
            if self.count_lives == 1:
                self.__save_game(False, window.level_number, window.level_id)
                return STATE_END
            self.__die(window.camera)
            return STATE_CONTINUE

        if sprite.collide_mask(self, window.princess):
            self.__save_game(True, window.level_number, window.level_id)
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

    def get_current_time(self) -> str:
        """Время, проведенное в игре"""
        return Mario.__get_str_time(time.perf_counter() - self.start_time)

    def __move(self, dt: int, blocks: List[MarioObject]) -> None:
        """Метод передвигает Марио
        :param dt: время в милисекундах
        :param blocks: лист с блоками
        """
        self.was_collide = False
        self.on_ground = False
        self.rect.y += MarioObject._direction_round(self.direction_y * dt / 100)
        self.__collide_with_blocks(0, self.direction_y, blocks)

        self.rect.x += MarioObject._direction_round(self.direction_x * dt / 100)
        self.__collide_with_blocks(self.direction_x, 0, blocks)

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
            self.image = self.images[6]

        if left:
            self.direction_x = -MARIO_SPEED
            if not up:
                self.image = self.images[0 + self.frame // 5]
                self.frame = (self.frame + 1) % 10
            else:
                self.image = self.images[5]
        elif right:
            self.direction_x = MARIO_SPEED
            if not up:
                self.image = self.images[2 + self.frame // 5]
                self.frame = (self.frame + 1) % 10
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
                              blocks: List[MarioObject]) -> None:
        """Определяем столкновения с блоками
        :param control_x: направление по x
        :param blocks: лист с блоками
        :param control_y: направление по y
        """
        for p in blocks:
            if sprite.collide_rect(self, p):

                if control_x > 0:  # вправо
                    self.rect.right = p.rect.left
                    self.was_collide = True

                if control_x < 0:  # влево
                    self.rect.left = p.rect.right
                    self.was_collide = True

                if control_y > 0:  # вниз
                    if isinstance(p, Teleport):
                        self.__teleporting(p)
                    else:
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

    def __collide_with_bonus(self, bonus: List[MarioObject]) -> None:
        """Пересечение марио с бонусом: монеткой или шишкой
        :param bonus: список всех бонусов в игре
        """
        for bon in bonus.copy():
            if sprite.collide_rect(self, bon):
                if isinstance(bon, Bump):
                    self.count_bumps += 2
                else:
                    self.count_money += 1

                bonus.remove(bon)

    def __save_game(self, is_win: bool, level_number: int, level_id: int) -> None:
        """Сохранение проигранного уровня в БД
        :param level_number: номер уровня
        """
        if not self.is_saving:
            global last_gid
            last_gid = save_game(is_win, self.get_current_time(), level_number, self.count_money, level_id)
            self.is_saving = True

    def __teleporting(self, teleport: Teleport) -> None:
        """Телепортируем Марио
        :param teleport: телепорт, на который наступил Марио
        """
        self.rect.x, self.rect.y = teleport.go_coords[0] + 20, teleport.go_coords[1] - 20

    def __die(self, camera):
        self.count_lives -= 1
        self.last_die = time.time()
        self.rect.x = self.coordinate[0] - MARIO_WIDTH // 2
        self.rect.y = self.coordinate[1] - MARIO_HEIGHT // 2 - 2
        camera.update(self)
        self.image = self.images[-1]

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
