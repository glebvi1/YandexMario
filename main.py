import pygame
from pygame.mixer import music
from pytmx import load_pygame

from config import HEIGHT, WIDTH, LEVEL1_PATH, MARIO_PATH, PRINCESS_PATH, \
    FIRE_PATH, BLOCKS_PATH, BACKGROUND_MUSIC_PATH, STATE_END, STATE_WIN
from config.Button import Button
from config.Camera import Camera
from models.Mario import Mario
from models.MarioObject import MarioObject
from models.MoveFire import MoveFire


class Level:
    def __init__(self, level_path: str, window):
        self.mario = None
        self.princess = None
        self.blocks = []
        self.enemies = []

        self.window = window

        self.map = load_pygame(level_path)
        self.tile_size = self.map.tilewidth

        self.load_game()

        self.camera = Camera(self.map.width * self.tile_size, self.map.height * self.tile_size)

        load_background_music()

    def load_game(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 0)
                if image is None:
                    continue
                mario_object_id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)]
                self.add_mario_object(mario_object_id, x, y)

    def add_mario_object(self, mo_id, x, y):
        coords = (x * self.tile_size, y * self.tile_size)

        if mo_id == 1:
            self.blocks.append(MarioObject(coords, BLOCKS_PATH))
        elif mo_id == 2:
            self.enemies.append(MoveFire(coords, FIRE_PATH, 50))
        elif mo_id == 3:
            self.princess = MarioObject(coords, PRINCESS_PATH)
        elif mo_id == 4:
            self.mario = Mario(coords, MARIO_PATH)

    def draw(self, screen):
        screen.fill((0, 200, 0))

        self.mario.draw(screen, self.camera)
        self.princess.draw(screen, self.camera)

        for widg in self.blocks:
            widg.draw(screen, self.camera)
        for widg in self.enemies:
            widg.draw(screen, self.camera)

    def update(self, delta_time, vector):
        state = self.mario.update(delta_time, vector, self)
        self.camera.update(self.mario)

        for widg in self.enemies:
            widg.update(delta_time)

        return state

    def quit(self):
        self.window = None


class Window:
    def __init__(self):
        self.running = True

        self.buttons = [
            Button((100, 100, 150, 50), "Level1")
        ]
        self.current_level = None

    def quit(self):
        print("quit")
        self.running = False

    def draw(self, screen):
        if self.current_level is not None:
            self.current_level.draw(screen)
        else:
            screen.fill((0, 200, 0))
            for widg in self.buttons:
                widg.draw(screen)

    def update(self, delta_time, vector, position, button):
        if self.current_level is not None:
            state = self.current_level.update(delta_time, vector)

            if state == STATE_END:
                print("Марио проиграл")
                self.quit()
            elif state == STATE_WIN:
                print("Марио выиграл")
                self.quit()

        else:
            for number, widg in enumerate(self.buttons):
                if widg.click(position, button):
                    self.current_level = Level(LEVEL1_PATH, self)


def load_background_music():
    music.load(BACKGROUND_MUSIC_PATH)
    music.play(-1, 0.0)


def main():
    coords = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(coords)
    pygame.display.set_caption("Супер Марио")

    game = Window()
    clock = pygame.time.Clock()

    fps = 60
    right = left = up = throw = False

    while game.running:
        button, position = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    up = True
                elif event.key == pygame.K_SPACE:
                    throw = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_SPACE:
                    throw = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position, button = event.pos, event.button

        game.draw(screen)
        game.update(clock.tick(fps), (right, left, up, throw), position, button)
        pygame.display.flip()


if __name__ == "__main__":
    main()
