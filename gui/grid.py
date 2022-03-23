import os
import pygame


class Grid:
    """
      This class represent a grid where the game
      is going to happen.
    """

    def __init__(self, pos_x: float, pos_y: float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load(
            os.path.join('assets', 'map', 'tiled_sea.png'))

    def draw(self, window: pygame.display) -> None:
        window.blit(self.image, (self.pos_x, self.pos_y))
