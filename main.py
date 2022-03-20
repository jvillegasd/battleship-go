from audioop import cross
import os
import pygame

from sprites.crosshair import Crosshair
from sprites.ships.carrier import Carrier

WIDTH, HEIGHT = 940, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')
pygame.mouse.set_visible(False)

# Color name: Little Greene French Grey Pale
BACKGROUND_COLOR = (231, 231, 219)

FPS = 60

SEA_MAP_IMAGE = pygame.image.load(
    os.path.join('assets', 'map', 'tiled_sea.png'))


def draw_window(crosshair_group):
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(SEA_MAP_IMAGE, (35, 45))
    
    crosshair_group.draw(WIN)
    crosshair_group.update()
    
    pygame.display.update()


def main():
    new_carrier = Carrier(35, 45)
    
    crosshair = Crosshair()
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)
  
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Force game loop to run at FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(crosshair_group)

    pygame.quit()


if __name__ == '__main__':
    main()
