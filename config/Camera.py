from config import WIDTH, HEIGHT
from pygame.rect import Rect


class Camera:
    def __init__(self, w, h):
        self.state = Rect(0, 0, w, h)

    def apply(self, obj):
        return obj.rect.move(self.state.topleft)

    def update(self, target):
        l = -(target.rect.x) + WIDTH // 2
        t = -(target.rect.y) + HEIGHT // 2
        w = self.state.width
        h = self.state.height

        self.state = Rect(l, t, w, h)
