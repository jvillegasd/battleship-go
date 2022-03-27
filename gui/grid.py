import os
import pygame
from typing import Tuple
from sprites.ship import Ship


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

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        # Inflate rect width to handle 'is_ship_inside' validation at boundaries
        self.rect = self.rect.inflate(20, 0)

    def get_tile_under_mouse(self) -> Tuple[int, int]:
        """
          This method calculates the current selected tile
          of the grid by mouse.
        """

        # Translate mouse position to grid space
        x, y = self.translate_position(pygame.mouse.get_pos())
        final_x, final_y = self.get_rescaled_dimensions()

        if x >= 0 and y >= 0 and x < final_x and y < final_y:
            return x, y
        else:
            return None, None

    def draw(self, window: pygame.display) -> None:
        """
          This method draws grid on window.
        """
        # Image is drawed using initial position due to self.rect is inflated
        window.blit(self.image, (self.pos_x, self.pos_y))
    
    def draw_selected_tile(self, window: pygame.display) -> None:
        """
          This method draws current selected tile
          if mouse is over grid on window.
        """

        square_x, square_y = self.get_tile_under_mouse()
        if square_x is not None:
            square_color = (255, 0, 0)
            square_pos = (self.pos_x + square_x * self.tile_size,
                          self.pos_y + square_y * self.tile_size)
            square_size = (self.tile_size, self.tile_size)
            pygame.draw.rect(window, square_color,
                             (square_pos, square_size), 2)

    def get_rescaled_dimensions(self) -> Tuple[float, float]:
        """
          This method re-scales grid dimension using tile_size in order
          to standardize coordinates.
        """
        return int(self.image.get_width() // self.tile_size), int(self.image.get_height() // self.tile_size)

    def translate_position(self, position: Tuple[int, int]) -> Tuple[float, float]:
        """
          This method translates (x, y) position into re-scaled grid.
        """

        grid_offset = (self.pos_x, self.pos_y)
        position_with_offset = pygame.Vector2(position) - grid_offset
        return int(position_with_offset[0] // self.tile_size), int(position_with_offset[1] // self.tile_size)

    def is_ship_inside(self, ship: Ship) -> bool:
        """
          This method checks if ship is completely inside in grid.
        """
        return self.rect.contains(ship.rect)
