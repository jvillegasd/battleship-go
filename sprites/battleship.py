import os
import pygame
from sprites.ship import Ship


class Battleship(Ship):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        image_path = os.path.join(
            'assets', 'ships', 'battleship', 'batleship.png')
        super().__init__(image_path, pos_x, pos_y)
