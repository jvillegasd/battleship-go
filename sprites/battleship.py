import os
import pygame
from gui.grid import Grid


class Battleship(pygame.sprite.Sprite):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        super().__init__()

        self.image = pygame.image.load(os.path.join(
            'assets', 'ships', 'battleship', 'batleship.png'))

        self.life = None
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def get_dimensions(self):
        return self.image.get_width(), self.image.get_height()
    
    

    def get_location_from_grid(self, grid: Grid):
        grid_width, grid_height = grid.get_dimensions()
        ship_width, ship_height = self.get_dimensions()

    def drag_and_drop(self, grid: Grid) -> None:
        pass
