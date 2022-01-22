from pygame.rect import Rect

from config import WIDTH, HEIGHT
from models.Mario import Mario


class Camera:
    def __init__(self, w, h):
        self.state = Rect(0, 0, w, h)
        self.w = w
        self.h = h

    def update(self, target: Mario):
        self.state.x = min(max(target.rect.x - WIDTH // 2, 0), self.w)
        self.state.y = min(max(target.rect.y - HEIGHT // 2, 0), self.h)
