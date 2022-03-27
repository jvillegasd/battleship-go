import pygame
from typing import Tuple
from gui.grid import Grid
from gui.button import Button


class Ship:
    """
      This class handles every ships common logic.
    """
    
    def __init__(self, image_path: str, pos_x: float, pos_y: float) -> None:
        self.image = pygame.image.load(image_path)
        self.life = None
        
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        self.can_rotate = True
        self.rotate_btn = Button(
            text='Rotate',
            pos_x=self.rect.center[0],
            pos_y=self.rect.center[1],
            width=70,
            height=30,
            btn_color='#AEC301',
            btn_bottom_color='#64734c',
            btn_hover_color='#637001'
        )
        self.rotate_btn.center_buttom_from_position(self.rect.center)

    def is_inside_grid(self, grid: Grid) -> bool:
        """
          This method checks if ship is completely inside in grid.
        """
        return grid.rect.contains(self.rect)
    
    def move_ship(self, delta: Tuple[float, float], grid: Grid) -> None:
        """
          This method moves ship by adding a delta to current
          rect position. If final position lets ship outside
          the grid, the ship is moved to inital position.
        """
        
        self.rect.x += delta[0]
        self.rect.y += delta[1]
        
        if not self.is_inside_grid(grid):
            self.rect.x -= delta[0]
            self.rect.y -= delta[1]
    
    def dragged_ship_position(self, grid: Grid) -> None:
        """
          This method calculates where to drop dragged ship in a valid 
          position of the grid.

          The main idea is to use ship.rect.center as a pivot in order to
          locate dragged ship. This pivot is going to be translated into
          grid space in order to get a valid position, them, this coordinates is
          upscaled and centered at tile.
        """

        grid_offset = (grid.pos_x, grid.pos_y)
        tile_center_offset = (int(grid.tile_size // 2),
                              int(grid.tile_size // 2))

        # Translate ship.rect.center position
        x, y = grid.translate_position(self.rect.center)

        # Take translated position and upscale it
        upscaled_x = x * grid.tile_size
        upscaled_y = y * grid.tile_size
        position_without_offset = pygame.Vector2(
            (upscaled_x, upscaled_y)) + grid_offset

        # Add another offset in order to locate ship.rect.center at center of the tile
        position_without_offset += tile_center_offset
        self.rect.center = position_without_offset
        
        self.rotate_btn.center_buttom_from_position(position_without_offset)
    
    def rotate_ship(self, grid: Grid) -> None:
        """
          This method rotates a ship and validates if 
          final position lets it inside the provided grid.
        """
        
        current_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center = current_center)
        
        if not self.is_inside_grid(grid):
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect(center = current_center)
    
    def draw(self, window: pygame.display) -> None:
        """
          This method draws ship on window.
        """
        window.blit(self.image, self.rect)
        self.draw_hitbox(window)

    def draw_hitbox(self, window: pygame.display) -> None:
        """
          This method draws ship rect and its center point on window.
        """
        
        width = self.image.get_width()
        height = self.image.get_height()
        pygame.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y, width, height), 1, border_radius=1)
        pygame.draw.circle(window, (255,0,0), self.rect.center, 4) 
