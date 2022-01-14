from pygame import font
from pygame.mixer import music
from pytmx import load_pygame

from config import MARIO_PATH, PRINCESS_PATH, FIRE_PATH, BLOCKS_PATH, QBLOCKS_PATH, FLY_DEATH_PATH, MONEY_PATH, \
    COLOR_TEXT_BUTTON, STATE_END, STATE_WIN, BACKGROUND_MUSIC_PATH
from config.Camera import Camera
from models.FlyDeath import FlyDeath
from models.Mario import Mario
from models.MarioObject import MarioObject, BaseMarioObject
from models.MoveFire import MoveFire
from models.QBlock import QBlock


class Level:
    def __init__(self, level_path: str, level_number: int):
        self.mario = None
        self.princess = None
        self.blocks = []
        self.enemies = []
        self.bonus = []

        self.background1 = []
        self.background2 = []


        self.level_number = level_number

        self.map = load_pygame(level_path)
        self.tile_size = self.map.tilewidth

        self.load_game()

        self.camera = Camera(self.map.width * self.tile_size, self.map.height * self.tile_size)

        Level.load_background_music()

    def load_game(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 0)
                if image is None:
                    continue
                tile_id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)]
                self.add_mario_object(tile_id, x, y)

    def add_mario_object(self, mo_id, x, y):
        coords = (x * self.tile_size, y * self.tile_size)

        if mo_id == 1:
            self.blocks.append(MarioObject(coords, BLOCKS_PATH))
        elif mo_id == 2:
            self.enemies.append(MoveFire(coords, FIRE_PATH))
        elif mo_id == 3:
            self.princess = MarioObject(coords, PRINCESS_PATH)
        elif mo_id == 4:
            self.mario = Mario(coords, MARIO_PATH)
        elif mo_id == 5:
            self.blocks.append(QBlock(coords, QBLOCKS_PATH))
        elif mo_id == 6:
            self.enemies.append(FlyDeath(coords, FLY_DEATH_PATH))
        elif mo_id == 7:
            self.bonus.append(MarioObject(coords, MONEY_PATH))

    def draw(self, screen) -> None:
        screen.fill((0, 200, 0))


        for widg in self.background1:
            widg.draw(screen, self.camera)
        for widg in self.background2:
            widg.draw(screen, self.camera)
        self.mario.draw(screen, self.camera)
        self.princess.draw(screen, self.camera)
        for widg in self.blocks:
            widg.draw(screen, self.camera)
        for widg in self.enemies:
            widg.draw(screen, self.camera)
        for widg in self.bonus:
            widg.draw(screen, self.camera)

        self.__draw_information(screen)

    def update(self, delta_time, vector) -> int:
        state = self.mario.update(delta_time, vector, self)
        self.camera.update(self.mario)

        for widg in self.enemies:
            widg.update(delta_time, self.blocks)
        if state in (STATE_END, STATE_WIN):
            music.stop()

        return state

    def __draw_information(self, screen) -> None:
        timer_text = font.Font(None, 36).render(self.mario.get_current_time(), True, COLOR_TEXT_BUTTON)
        bumps_text = f"Шишки X {self.mario.count_bumps}"
        bumps_text = font.Font(None, 36).render(bumps_text, True, COLOR_TEXT_BUTTON)

        screen.blit(timer_text, (0, 0, 150, 50))
        screen.blit(bumps_text, (100, 0, 150, 50))

    @staticmethod
    def load_background_music():
        music.load(BACKGROUND_MUSIC_PATH)
        music.play(-1, 0.0)


class LevelWithLayers(Level):
    def load_game(self):
        for layer in range(3):
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, layer)
                    if image is not None:
                        tile_id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, layer)]
                        self.add_mario_object(tile_id, x, y, image)

    def add_mario_object(self, mo_id, x, y, image):
        coords = (x * self.tile_size, y * self.tile_size)


        if mo_id == 595:
            self.mario = Mario(coords, MARIO_PATH)
        elif mo_id == 596:
            self.princess = MarioObject(coords, PRINCESS_PATH)
        elif 198 < mo_id <= 269 or mo_id == 479:
            self.background1.append(BaseMarioObject(coords, image))
        elif mo_id in [27, 28, 29, 30, 31, 155, 40, 41, 42, 43, 44, 53, 54, 55, 56, 57, 66, \
                       67, 68, 69, 70, 79, 80, 81, 82, 83, 14, 15, 16, 17, 18, 92, 93, 94, 95,\
                       96, 20, 19]:
            self.background2.append(BaseMarioObject(coords, image))
        elif mo_id == 593:
            self.enemies.append(MoveFire(coords, FIRE_PATH))
        elif mo_id == 591:
            self.blocks.append(QBlock(coords, QBLOCKS_PATH))
        elif mo_id == 594:
            self.enemies.append(FlyDeath(coords, FLY_DEATH_PATH))
        elif mo_id == 592:
            self.bonus.append(MarioObject(coords, MONEY_PATH))
        elif mo_id in [10, 180, 189]:
            self.blocks.append(BaseMarioObject(coords, image))
