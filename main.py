import pygame
from models.Mario import Mario
from models.Blocks import Block
from models.MarioObject import MarioObject
from models.Fire import Fire


class MainWindow:
    def __init__(self):
        self.running = True
        self.mario = Mario((100, 100), "res/heros/0.png")
        self.princess = MarioObject((200+32*4, 152), "res/heros/princess.png")

        self.blocks = [
            MarioObject((200, 100), "res/blocks/block.png"),
            Block((200, 132), "res/blocks/block.png"),
            Block((200, 164), "res/blocks/block.png"),
            Block((200, 186), "res/blocks/block.png"),
            Block((200+32, 186), "res/blocks/block.png"),
            Block((200+32*2, 186), "res/blocks/block.png"),
            Block((200+32*3, 186), "res/blocks/block.png"),
            Block((200+32*4, 186), "res/blocks/block.png"),
            Block((200-32, 186), "res/blocks/block.png"),
            Block((200-32*2, 186), "res/blocks/block.png"),
            Block((200-32*3, 186), "res/blocks/block.png"),
            Block((200-32*4, 186), "res/blocks/block.png")
        ]
        self.enemies = [
            Fire((200 + 32 * 2, 186 - 32), "res/enemies/fire.png")
        ]

    def quit(self):
        self.running = False

    def draw(self, screen):
        screen.fill((0, 200, 0))
        self.mario.draw(screen)
        self.princess.draw(screen)
        for widg in self.blocks:
            widg.draw(screen)
        for widg in self.enemies:
            widg.draw(screen)

    def update(self, delta_time, vector):
        if not self.mario.update(delta_time, vector, self.blocks):
            self.quit()

        for widg in self.blocks:
            widg.update(delta_time)
        for widg in self.enemies:
            widg.update(delta_time)


if __name__ == "__main__":
    coords = 700, 600
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
                print("quit")
                game.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE\
                        or event.key == pygame.K_UP:
                    up = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE\
                        or event.key == pygame.K_UP:
                    up = False

        game.draw(screen)
        game.update(clock.tick(fps), (right, left, up))
        pygame.display.flip()
