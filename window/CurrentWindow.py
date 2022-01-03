from config import LEVEL1_PATH, STATE_END, STATE_WIN
from dao.db_mario_handler import get_win_level_number
from window.Button import Button
from window.Level import Level


class CurrentWindow:
    def __init__(self):
        self.running = True

        self.buttons = []
        self.__set_buttons()
        self.current_level = None

    def __set_buttons(self):
        self.buttons = [
            Button((100, 100, 150, 50), "Уровень 1"),
            Button((100, 200, 150, 50), "Уровень 2"),
            Button((100, 300, 150, 50), "Уровень 3"),
            Button((100, 400, 150, 50), "Уровень 4"),
        ]
        win_levels = get_win_level_number()
        for number, time in win_levels:
            self.buttons[number - 1].set_win_color()
            self.buttons[number - 1].set_text_description(time)

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
                self.current_level = None
                self.__set_buttons()
            elif state == STATE_WIN:
                print("Марио выиграл")
                self.current_level = None
                self.__set_buttons()

        else:
            for number, widg in enumerate(self.buttons):
                if widg.click(position, button):
                    self.current_level = Level(LEVEL1_PATH, number + 1)

    def quit(self):
        print("quit")
        self.running = False
