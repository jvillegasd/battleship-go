import os
from sprites.ship import Ship


class Battleship(Ship):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        image_path = os.path.join(
            'assets', 'ships', 'battleship', 'batleship.png')
        super().__init__(image_path, pos_x, pos_y)
        
        self.inflate_value = (-15, 0)
        self.collision_rect = self.rect.inflate(self.inflate_value)
