from config import LEVEL1_PATH, LEVEL2_PATH, LEVEL3_PATH, LEVEL4_PATH, LEVEL5_PATH, STATE_END, \
     STATE_WIN
from dao.db_mario_handler import get_level_number_by_win
from window.Button import Button
from window.Level import Level, Level2, Level3, Level4, Level5


class CurrentWindow:
    def __init__(self):
        self.running = True

        self.buttons = []
        self.__set_buttons()
        self.current_level = None

    def __set_buttons(self):
        self.buttons = [
            Button((100, 100, 220, 50), "Уровень 1"),
            Button((100, 200, 220, 50), "Уровень 2"),
            Button((100, 300, 220, 50), "Уровень 3"),
            Button((100, 400, 220, 50), "Уровень 4"),
            Button((100, 500, 220, 50), "Уровень 5"),
        ]
        win_levels = get_level_number_by_win(is_win=True)
        for number, time, count_bumps in win_levels:
            self.buttons[number - 1].set_win_color()
            text_description = f"Время: {time}, монетки: {count_bumps}"
            self.buttons[number - 1].set_text_description(text_description)

        lose_levels = get_level_number_by_win(is_win=False)
        for number, time, count_bumps in lose_levels:
            self.buttons[number - 1].set_lose_color()
            text_description = f"Время: {time}, монетки: {count_bumps}"
            self.buttons[number - 1].set_text_description(text_description)

    def draw(self, screen):
        if self.current_level is not None:
            self.current_level.draw(screen)
        else:
            screen.fill((200, 100, 50))
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
                    if number == 0:
                        self.current_level = Level(LEVEL1_PATH, number + 1)
                        #Level.load_background_music(MUS_PATH1)
                    elif number == 1:
                        self.current_level = Level2(LEVEL2_PATH, number + 1)
                        #Level.load_background_music(MUS_PATH2)
                    elif number == 2:
                        self.current_level = Level3(LEVEL3_PATH, number + 1)
                        #Level.load_background_music(MUS_PATH3)
                    elif number == 3:
                        self.current_level = Level4(LEVEL4_PATH, number + 1)
                        #Level.load_background_music(MUS_PATH4)
                    elif number == 4:
                        self.current_level = Level5(LEVEL5_PATH, number + 1)
                        #Level.load_background_music(MUS_PATH5)

    def quit(self):
        print("quit")
        self.running = False
