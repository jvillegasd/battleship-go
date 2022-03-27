import os
from sprites.ship import Ship


class Submarine(Ship):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        image_path = os.path.join(
            'assets', 'ships', 'submarine', 'submarine.png')
        super().__init__(image_path, pos_x, pos_y)
