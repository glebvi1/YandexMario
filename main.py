import pygame

from config import HEIGHT, WIDTH, CAPTION, FPS
from window.CurrentWindow import CurrentWindow


def main():
    coords = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(coords)
    pygame.display.set_caption(CAPTION)

    game = CurrentWindow()
    clock = pygame.time.Clock()

    right = left = up = throw = music_play = False

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
                elif event.key == pygame.K_p:
                    music_play = not music_play

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
        game.update(clock.tick(FPS), (right, left, up, throw), position, button, music_play)
        pygame.display.flip()


if __name__ == "__main__":
    main()
