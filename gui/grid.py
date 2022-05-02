import enum
import os
import pygame
from typing import Tuple

SHIPS_NAMES = ['B', 'C', 'D', 'R', 'S']


class Grid:
    """
      This class represent a grid where the game
      is going to happen. Grid uses a fixed map image
      and its tile pixel size is 16. It means that every
      tile of map image is 16x16.

      Grid image size is 320x320, so game grid is a 20x20
      2D array.
    """

    def __init__(self, pos_x: float, pos_y: float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.image.load(
            os.path.join('assets', 'map', 'tiled_sea.png'))

        self.tile_size = 16
        self.game_grid_cols = 20
        self.game_grid_rows = 20

        self.game_grid = [
            [0 for i in range(self.game_grid_cols)] for j in range(self.game_grid_rows)]

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        # Inflate rect width to handle 'is_ship_inside' validation at boundaries
        self.rect = self.rect.inflate(12, 10)

    def get_tile_under_mouse(self) -> Tuple[int, int]:
        """
          This function calculates the current selected tile
          of the grid by mouse.
        """

        # Translate mouse position to grid space
        x, y = self.translate_position(pygame.mouse.get_pos())
        if self.is_valid_position((x, y)):
            return x, y
        else:
            return None, None

    def draw(self, window: pygame.display) -> None:
        """
          This function draws grid on window.
        """

        # Image is drawed using initial position due to self.rect is inflated
        window.blit(self.image, (self.pos_x, self.pos_y))

    def draw_hitbot(self, window: pygame.display) -> None:
        """
          This function draws grid rect on window.
        """
        pygame.draw.rect(window, (255, 0, 0), (self.rect.x, self.rect.y,
                         self.rect.width, self.rect.height), 1, border_radius=1)

    def draw_selected_tile(self, window: pygame.display) -> None:
        """
          This function draws current selected tile
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
          This function re-scales grid dimension using tile_size in order
          to standardize coordinates.
        """
        return int(self.image.get_width() // self.tile_size), int(self.image.get_height() // self.tile_size)

    def translate_position(self, position: Tuple[float, float]) -> Tuple[float, float]:
        """
          This function translates (x, y) position into re-scaled grid.
        """

        grid_offset = (self.pos_x, self.pos_y)
        position_with_offset = pygame.Vector2(position) - grid_offset
        return int(position_with_offset[0] // self.tile_size), int(position_with_offset[1] // self.tile_size)

    def upscale_position(self, position: Tuple[float, float]) -> Tuple[float, float]:
        """ This function upscales the provided position. """
        
        grid_offset = (self.pos_x, self.pos_y)
        
        upscaled_x = position[0] * self.tile_size
        upscaled_y = position[1] * self.tile_size
        
        position_without_offset = pygame.Vector2(
            (upscaled_x, upscaled_y)) + grid_offset
        
        return position_without_offset

    def center_position(self, position: Tuple[float, float]) -> Tuple[float, float]:
        """
          This function readjust and upscales the provided position
          to the center of the tile it falls.

          The position is going to be translated into grid space
          in order to get a valid position, them, this coordinates
          is upscaled and centered at tile.
        """
        
        tile_center_offset = (int(self.tile_size // 2),
                              int(self.tile_size // 2))

        # Translate ship.rect.center position
        x, y = self.translate_position(position)

        # Take translated position and upscale it
        position_without_offset = self.upscale_position((x, y))

        # Add another offset in order to locate ship.rect.center at center of the tile
        position_without_offset += tile_center_offset

        return position_without_offset

    def locate_ships_into_game_grid(self, ships: list) -> list:
        """
          This function locates ships into game grid in order
          to manage game state.

          The main idea is to use ship.rect.center as a pivot in order to
          locate the ship on the game grid around this position. The number
          of tiles used by the ship on the grid is calculated by dividing its
          collision_rect height or width (depeding on orientation) by tile_size.
          This value is used together with translated ship.rec.center position
          to fill the game grid.
        """

        for index, ship in enumerate(ships):
            ship_life = 0
            x, y = self.translate_position(ship.rect.center)
            
            if ship.is_vertical:
                collision_rect_height = ship.collision_rect.height
                number_of_tiles = int(collision_rect_height // self.tile_size)

                # Locate ship vertically by using translated position as a pivot
                for i in range(int(number_of_tiles // 2)):
                    if y - i >= 0:
                        if self.game_grid[y - i][x] == 0:
                            ship_life += 1
                        
                        self.game_grid[y - i][x] = ship.name

                    if y + i < self.game_grid_rows:
                        if self.game_grid[y + i][x] == 0:
                            ship_life += 1
                        
                        self.game_grid[y + i][x] = ship.name
            else:
                collision_rect_width = ship.collision_rect.width
                number_of_tiles = int(collision_rect_width // self.tile_size)

                # Locate ship horizontally by using translated position as a pivot
                for i in range(int(number_of_tiles // 2)):
                    if x - i >= 0:
                        if self.game_grid[y][x - i] == 0:
                            ship_life += 1
                        
                        self.game_grid[y][x - i] = ship.name

                    if x + i < self.game_grid_cols:
                        if self.game_grid[y][x + i] == 0:
                            ship_life += 1
                        
                        self.game_grid[y][x + i] = ship.name

            ships[index].set_ship_life(ship_life)
        return ships

    def attack_tile(self, position: Tuple[float, float]) -> Tuple[bool, str]:
        """
          This function evaluates if a ship is located
          at selected tile in order to attack it.
        """

        # Translate mouse position to grid space
        x, y = self.translate_position(position)
        if self.is_valid_position((x, y)):
            if self.game_grid[y][x] in SHIPS_NAMES:
                self.game_grid[y][x] = 1
                return True, self.game_grid[y][x]

        return False, ''

    def is_valid_position(self, position: Tuple[float, float]) -> bool:
        """
          This function validates if provided position is
          inside re-scaled grid.
        """

        final_x, final_y = self.get_rescaled_dimensions()
        return (position[0] >= 0 and position[1] >= 0 and
                position[0] < final_x and position[1] < final_y)
