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


def draw_window(sprite_groups):
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(SEA_MAP_IMAGE, (35, 45))

    for _, sprite_group in sprite_groups.items():
        sprite_group.draw(WIN)
        sprite_group.update()

    pygame.display.update()


def main():
    # Adding ship sprites
    new_carrier = Carrier(35, 45)
    ships_group = pygame.sprite.Group()
    ships_group.add(new_carrier)

    # Adding remaining sprites
    crosshair = Crosshair()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(crosshair)
    
    # Handle sprite group painting dynamically
    sprite_groups = {
      'ships': ships_group,
      'all': all_sprites
    }

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Force game loop to run at FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(sprite_groups)

    pygame.quit()


if __name__ == '__main__':
    main()
