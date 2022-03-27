import os
from sprites.ship import Ship


class RescueShip(Ship):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        image_path = os.path.join(
            'assets', 'ships', 'rescue_ship', 'rescue_ship.png')
        super().__init__(image_path, pos_x, pos_y)
