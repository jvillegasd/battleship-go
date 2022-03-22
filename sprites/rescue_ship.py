import os
import pygame


class RescueShip(pygame.sprite.Sprite):

    def __init__(self, pos_x: float, pos_y: float) -> None:
        super().__init__()

        self.image = pygame.image.load(os.path.join(
            'assets', 'ships', 'rescue_ship', 'rescue_ship.png'))

        self.life = None
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
