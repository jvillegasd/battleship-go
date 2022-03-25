import os
import pygame
from typing import Tuple
from gui.grid import Grid


class Battleship(pygame.sprite.Sprite):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        super().__init__()

        self.image = pygame.image.load(os.path.join(
            'assets', 'ships', 'battleship', 'batleship.png'))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.life = None
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def drag_and_drop(self, grid: Grid) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if grid.is_ship_inside(self):
          if self.rect.collidedict(mouse_pos):
            pass
