import pygame

from config import HEIGHT, WIDTH, CAPTION, FPS
from window.CurrentWindow import CurrentWindow
from window.LoginWindow import LoginWindow


def main():
    coords = WIDTH, HEIGHT
    pygame.init()
    screen = pygame.display.set_mode(coords)
    pygame.display.set_caption(CAPTION)

    game = CurrentWindow()
    login = LoginWindow()
    clock = pygame.time.Clock()

    right = left = up = throw = is_quit = False
    music_play = True

    while game.running:
        button, position = 0, 0
        login_event = None

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
                elif event.key == pygame.K_ESCAPE:
                    is_quit = True
                login_event = event

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_SPACE:
                    throw = False
                elif event.key == pygame.K_ESCAPE:
                    is_quit = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position, button = event.pos, event.button
                if not login.is_authorizing:
                    login.activated_input(position)

        if login.is_authorizing:
            game.draw(screen)
            game.update(clock.tick(FPS), (right, left, up, throw), position, button, (music_play, is_quit))
        else:
            login.draw(screen)
            login.update(login_event, position, button)
        pygame.display.flip()


if __name__ == "__main__":
    main()
