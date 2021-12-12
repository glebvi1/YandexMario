import pygame
from models.Mario import Mario
from models.Blocks import Block


class MainWindow:
    def __init__(self):
        self.running = True
        self.mario = Mario((250, 100), "res/mario/0.png")
        self.objects = [
            Block((300, 100), "res/blocks/block.png"),
            Block((300, 132), "res/blocks/block.png"),
            Block((300, 164), "res/blocks/block.png"),
            Block((200, 100), "res/blocks/block.png"),
            Block((200, 200), "res/blocks/block.png"),
            Block((232, 200), "res/blocks/block.png"),
            Block((264, 200), "res/blocks/block.png")
        ]

    def quit(self):
        self.running = False

    def draw(self, screen):
        screen.fill((0, 200, 0))
        self.mario.draw(screen)
        for widg in self.objects:
            widg.draw(screen)

    def update(self, delta_time, direction_x, direction_y):
        self.mario.update(direction_x, direction_y, self.objects)
        for widg in self.objects:
            widg.update(delta_time)


if __name__ == "__main__":
    coords = 800, 600
    pygame.init()
    screen = pygame.display.set_mode(coords)
    game = MainWindow()
    clock = pygame.time.Clock()
    fps = 60

    direction_x = 0
    direction_y = 0

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    direction_x = -1
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    direction_x = 1
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    direction_y = 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    direction_x = 0
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    direction_x = 0
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    direction_y = 0

        game.draw(screen)
        game.update(clock.tick(fps), direction_x, direction_y)
        pygame.display.flip()
