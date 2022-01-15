from config import WIDTH, HEIGHT
from pygame.rect import Rect
from models.Mario import Mario


class Camera:
    def __init__(self, w, h):
        self.state = Rect(0, 0, w, h)

    def update(self, target: Mario):
        self.state.x = target.rect.x - WIDTH // 2
        self.state.y = target.rect.y - HEIGHT // 2

