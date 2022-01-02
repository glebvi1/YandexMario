from pygame import font, draw

from config import COLOR_TEXT_BUTTON, COLOR_WIN_BUTTON, COLOR_LOSE_BUTTON


class Button:
    def __init__(self, button_coords: tuple[int, int, int, int], text):
        self.button_coords = button_coords
        f1 = font.Font(None, 36)
        self.text = f1.render(text, True, COLOR_TEXT_BUTTON)
        self.color = COLOR_LOSE_BUTTON

    def draw(self, screen):
        draw.rect(screen, self.color, self.button_coords)
        screen.blit(self.text, self.button_coords)

    def set_win_color(self):
        self.color = COLOR_WIN_BUTTON

    def click(self, position, button) -> bool:
        if 1 != button:
            return False
        if self.button_coords[0] <= position[0] <= self.button_coords[0] + self.button_coords[2] \
                and self.button_coords[1] <= position[1] <= self.button_coords[1] + self.button_coords[3]:
            return True
        return False
