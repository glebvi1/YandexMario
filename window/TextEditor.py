import pygame
from pygame import Color


class TextEditor:
    def __init__(self, coordinates, max_text_len=10, default_text=""):
        self.coordinates = coordinates
        self.editor = pygame.Rect(*coordinates)
        self.max_text_len = max_text_len
        self.is_active = False
        self.text = default_text
        self.active_color = Color(141, 182, 205)
        self.passive_color = Color(30, 144, 255)

    def draw(self, screen):
        color = self.active_color if self.is_active else self.passive_color

        font = pygame.font.Font(None, 40)
        txt_surface = font.render(self.text, True, color)

        screen.blit(txt_surface, (self.editor.x + 5, self.editor.y + 5))
        pygame.draw.rect(screen, color, self.editor, 2)

    def update(self, event) -> bool:
        if len(self.text) == self.max_text_len and event.key != pygame.K_BACKSPACE:
            return False

        if self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

        return True

    def activated(self, position):
        if self.editor.collidepoint(position):
            self.is_active = True
        else:
            self.is_active = False
