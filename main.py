import pygame
from models.Mario import Mario
from models.MarioObject import MarioObject
from models.MoveFire import MoveFire
from models import STATE_END, STATE_WIN
from config import HEIGHT, WIDTH
from config.Camera import Camera


class MainWindow:
    def __init__(self):
        self.running = True

        self.mario = Mario((100, 100), "res/heros/0.png")
        self.princess = MarioObject((600, 152-20), "res/heros/princess.png")

        self.blocks = []
        self.enemies = [
            MarioObject((200 + 32 * 5, 186), "res/enemies/fire.png"),
            MoveFire((200 + 32 * 2, 186 - 32), "res/enemies/fire.png", 100)
        ]
        self.level = [
            "-----------------------------------------",
            "                                         ",
            "                                         ",
            "        -                                ",
            "        -                                ",
            "------------   -------------------       ",
            "                                         ",
            "                      -                  ",
            "                    -                    ",
            "                    --                   ",
            "         -                               ",
            "                  ----                   ",
            "        ---     -                        ",
            "                -                        ",
            "-----------------------------------------",
            "                                         ",
        ]
        x = 0
        y = 0
        for a in self.level:
            for elem in a:
                if elem == "-":
                    block = MarioObject((x, y), "res/blocks/block.png")
                    self.blocks.append(block)
                x += 32
            x = 0
            y += 32

        self.camera = Camera(len(self.level[0])*32, len(self.level)*32)

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
