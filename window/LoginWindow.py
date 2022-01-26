import pygame
from config import COLOR_BACKGROUND
from dao.db_user_handler import registration_user, login_user
from window.Button import Button
from window.TextEditor import TextEditor


class LoginWindow:
    def __init__(self):
        self.login_window = True
        self.is_authorizing = False

        self.editor_name = TextEditor((20, 150, 200, 50), default_text="Имя")
        self.editor_login = TextEditor((20, 210, 200, 50), default_text="Логин")
        self.editor_password = TextEditor((20, 270, 200, 50), default_text="Пароль")
        self.button_ok = Button((20, 350, 270, 40), "Авторизоваться", color=(64, 32, 100))
        self.button_change_window = Button((400, 350, 270, 40), "Зарегистрироваться", color=(64, 32, 100))

        self.editors = (self.editor_name, self.editor_login, self.editor_password)

        self.error_text = ""

    def draw(self, screen):
        screen.fill(COLOR_BACKGROUND)

        if not self.login_window:
            self.editor_name.draw(screen)
        self.editor_login.draw(screen)
        self.editor_password.draw(screen)

        self.button_ok.draw(screen)
        self.button_change_window.draw(screen)

        font = pygame.font.Font(None, 40)
        txt_surface = font.render(self.error_text, True, (64, 32, 100))
        screen.blit(txt_surface, (100, 100))

    def update(self, event, position, button):
        if event is not None:
            for editor in self.editors:
                if not editor.update(event):
                    self.error_text = "Слишком много символов"

        if self.button_ok.click(position, button) and self.login_window:
            return self.__login()
        elif self.button_ok.click(position, button) and not self.login_window:
            return self.__reg()

        if self.button_change_window.click(position, button):
            self.login_window = not self.login_window
            if self.login_window:
                self.button_ok.set_text("Авторизоваться")
                self.button_change_window.set_text("Зарегистрироваться")
            else:
                self.button_change_window.set_text("Авторизоваться")
                self.button_ok.set_text("Зарегистрироваться")

    def activated_input(self, position):
        for editor in self.editors:
            editor.activated(position)

    def __reg(self):
        user = registration_user(self.editor_login.text, self.editor_name.text, self.editor_password.text)
        if user is None:
            self.error_text = "Ошибка регистрации"
            return None
        self.is_authorizing = True
        return user

    def __login(self):
        user = login_user(self.editor_login.text, self.editor_password.text)

        if user is None:
            self.error_text = "Ошибка авторизации"
            return None
        self.is_authorizing = True
        return user
