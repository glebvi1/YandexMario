import pygame
from models.Mario import Mario
from models.MarioObject import MarioObject
from models.MoveFire import MoveFire
from models import STATE_END, STATE_WIN
from config import HEIGHT, WIDTH
from config.Camera import Camera
from config import LEVEL1_PATH, MARIO_PATH, PRINCESS_PATH, FIRE_PATH, BLOCKS_PATH

from pytmx import load_pygame


class MainWindow:
    def __init__(self):
        self.running = True

        self.mario = None
        self.princess = None
        self.blocks = []
        self.enemies = []

        self.map = load_pygame(LEVEL1_PATH)
        self.tile_size = self.map.tilewidth

        self.load_game()

        self.camera = Camera(self.map.width * self.tile_size, self.map.height * self.tile_size)

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

    def quit(self):
        print("quit")
        self.running = False

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

        if state == STATE_END:
            print("Марио проиграл")
            pygame.quit()
        if state == STATE_WIN:
            print("Марио выиграл")
            pygame.quit()

        self.camera.update(self.mario)

        for widg in self.enemies:
            widg.update(delta_time)


def main():
    coords = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(coords)
    pygame.display.set_caption("Супер Марио")

    game = MainWindow()
    clock = pygame.time.Clock()

    fps = 60
    right = left = up = False

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE \
                        or event.key == pygame.K_UP:
                    up = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE \
                        or event.key == pygame.K_UP:
                    up = False

        game.draw(screen)
        game.update(clock.tick(fps), (right, left, up))
        pygame.display.flip()


if __name__ == "__main__":
    main()
