from config import LEVEL1_PATH, STATE_END, STATE_WIN
from config.Button import Button
from dao.db_mario_handler import get_win_level_number
from window.Level import Level


class CurrentWindow:
    def __init__(self):
        self.running = True

        self.buttons = [
            Button((100, 100, 150, 50), "Level1"),
            Button((100, 200, 150, 50), "Level2"),
            Button((100, 300, 150, 50), "Level3"),
            Button((100, 400, 150, 50), "Level4"),
        ]
        self.__set_color_buttons()
        self.current_level = None

    def __set_color_buttons(self):
        win_levels = get_win_level_number()
        for number in win_levels:
            self.buttons[number[0] - 1].set_win_color()

    def draw(self, screen):
        if self.current_level is not None:
            self.current_level.draw(screen)
        else:
            screen.fill((0, 200, 0))
            for widg in self.buttons:
                widg.draw(screen)

    def update(self, delta_time, vector, position, button):
        if self.current_level is not None:
            state = self.current_level.update(delta_time, vector)

            if state == STATE_END:
                print("Марио проиграл")
                self.quit()
            elif state == STATE_WIN:
                print("Марио выиграл")
                self.quit()

        else:
            for number, widg in enumerate(self.buttons):
                if widg.click(position, button):
                    self.current_level = Level(LEVEL1_PATH, number + 1)

    def quit(self):
        print("quit")
        self.running = False
