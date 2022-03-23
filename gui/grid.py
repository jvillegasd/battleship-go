import os
import pygame


class Grid:
    """
      This class represent a grid where the game
      is going to happen. Grid uses a fixed map image
      and its tile pixel size is 16. It means that every
      tile of map image is 16x16.
    """

    def __init__(self, pos_x: float, pos_y: float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.tile_size = 16
        self.image = pygame.image.load(
            os.path.join('assets', 'map', 'tiled_sea.png'))

    def draw(self, window: pygame.display) -> None:
        window.blit(self.image, (self.pos_x, self.pos_y))

    def calculate_grid(self) -> None:
        print(self.image.get_width(), self.image.get_height())
