import os
import pygame


class Crosshair(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join(
            'assets', 'crosshair', 'crosshair_red_small.png'))
        self.rect = self.image.get_rect()
        
    def update(self):
      self.rect.center = pygame.mouse.get_pos()
