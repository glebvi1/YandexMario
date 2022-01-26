from config import COLOR_BACKGROUND
from window.Button import Button
from window.TextEditor import TextEditor
from dao.db_user_handler import registration_user


class LoginWindow:
    def __init__(self):
        self.login_window = True
        self.is_authorizing = False

        self.editor_name = TextEditor((100, 150, 150, 50), default_text="Имя")
        self.editor_login = TextEditor((100, 210, 150, 50), default_text="Логин")
        self.editor_password = TextEditor((100, 270, 150, 50), default_text="Пароль")
        self.button_ok = Button((100, 350, 100, 40), "ОК", color=(64, 32, 100))

        self.editors = (self.editor_name, self.editor_login, self.editor_password)

    def draw(self, screen):
        screen.fill(COLOR_BACKGROUND)

        for editor in self.editors:
            editor.draw(screen)

        self.button_ok.draw(screen)

    def update(self, event, position, button):
        if event is not None:
            for editor in self.editors:
                editor.update(event)
        if self.button_ok.click(position, button):
            user = registration_user(self.editor_login.text, self.editor_name.text, self.editor_password.text)
            if user is None:
                #error
                pass
            else:
                self.is_authorizing = True

    def activated_input(self, position):
        for editor in self.editors:
            editor.activated(position)
