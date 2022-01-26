from pygame import font, draw

from config import COLOR_TEXT_BUTTON, COLOR_WIN_BUTTON, COLOR_LOSE_BUTTON, COLOR_NEUTRAL_BUTTON


class Button:
    def __init__(self, button_coords: tuple[int, int, int, int], text: str, text_description="", color=None):
        self.button_coords = button_coords
        self.text = font.Font(None, 36).render(text, True, COLOR_TEXT_BUTTON)
        self.text_description = font.Font(None, 18).render(text_description, True, COLOR_TEXT_BUTTON)
        self.text_description_coords = (button_coords[0], button_coords[1] + button_coords[3] // 2,
                                        button_coords[2], button_coords[3])
        if color is None:
            self.color = COLOR_NEUTRAL_BUTTON
        else:
            self.color = color

    def draw(self, screen):
        draw.rect(screen, self.color, self.button_coords)
        screen.blit(self.text, self.button_coords)
        screen.blit(self.text_description, self.text_description_coords)

    def set_win_color(self):
        self.color = COLOR_WIN_BUTTON

    def set_lose_color(self):
        self.color = COLOR_LOSE_BUTTON

    def set_text_description(self, text_description):
        self.text_description = font.Font(None, 25).render(text_description, True, COLOR_TEXT_BUTTON)

    def click(self, position, button) -> bool:
        if 1 != button:
            return False
        if self.button_coords[0] <= position[0] <= self.button_coords[0] + self.button_coords[2] \
                and self.button_coords[1] <= position[1] <= self.button_coords[1] + self.button_coords[3]:
            return True
        return False
