from config import LEVEL1_PATH, STATE_END, STATE_WIN
from config.Button import Button
from window.Level import Level


class CurrentWindow:
    def __init__(self):
        self.running = True

        self.buttons = [
            Button((100, 100, 150, 50), "Level1")
        ]
        self.current_level = None

    def quit(self):
        print("quit")
        self.running = False

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
                    self.current_level = Level(LEVEL1_PATH)
