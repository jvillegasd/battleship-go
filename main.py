import os
import pygame

WIDTH, HEIGHT = 930, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')

# Color name: Little Greene French Grey Pale
BACKGROUND_COLOR = (231, 231, 219)

FPS = 60

SEA_MAP_IMAGE = pygame.image.load(
    os.path.join('assets', 'map', 'tiled_sea.png'))


def draw_window():
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(SEA_MAP_IMAGE, (35, 45))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()


if __name__ == '__main__':
    main()
