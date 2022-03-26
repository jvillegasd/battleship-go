import os
import pygame
from typing import Tuple
from gui.grid import Grid


class Battleship:

    def __init__(self, pos_x: float, pos_y: float) -> None:
        self.image = pygame.image.load(os.path.join(
            'assets', 'ships', 'battleship', 'batleship.png'))
        self.life = None
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def move_ship(self, delta: Tuple[float, float]) -> None:
        self.rect.x += delta[0]
        self.rect.y += delta[1]
    
    def draw(self, window):
        # window.blit(self.image, self.rect)
        
        width = self.image.get_width()
        height = self.image.get_height()
        pygame.draw.rect(window, (255,0,0), (self.rect.x, self.rect.y, width, height), 1, border_radius=1)
        pygame.draw.circle(window, (255,0,0), self.rect.center, 4) 
