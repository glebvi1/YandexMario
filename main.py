import pygame

from config import HEIGHT, WIDTH
from window.CurrentWindow import CurrentWindow


def main():
    coords = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(coords)
    pygame.display.set_caption("Супер Марио")

    game = CurrentWindow()
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
