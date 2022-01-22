from math import ceil, floor

from pygame import sprite, image


class BaseMarioObject(sprite.Sprite):
    def __init__(self, coordinate, mo_image) -> None:
        """Базовый класс для любого объекта игры
        :param coordinate: начальные координаты спрайта
        :param mo_image: путь к картинке
        """
        sprite.Sprite.__init__(self)
        self.coordinate = coordinate

        self.image = mo_image
        self.rect = self.image.get_rect(center=(coordinate[0], coordinate[1]))

    def draw(self, screen, camera) -> None:
        """Отрисовываем спрайт
        :param screen: экран игры
        :param camera: камера
        """
        screen.blit(self.image, (self.rect.x - camera.state.x, self.rect.y - camera.state.y))

    @staticmethod
    def _direction_round(direction) -> int:
        """Метод округляет направление до целого числа
        :param direction: направление
        """
        return ceil(direction) if direction > 0 else floor(direction)


class MarioObject(BaseMarioObject):
    def __init__(self, coordinate: tuple, image_path: str) -> None:
        super().__init__(coordinate, image.load(image_path).convert_alpha())
