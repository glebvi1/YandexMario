from models.Hero import Hero


class Fire(Hero):
    def __init__(self, coordinates: tuple, image_path: str):
        super().__init__(coordinates, image_path, life=1)

