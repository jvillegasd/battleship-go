import os
import pygame

from gui.button import Button
from sprites.carrier import Carrier

WIDTH, HEIGHT = 940, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')

# Color name: Little Greene French Grey Pale
BACKGROUND_COLOR = (231, 231, 219)

FPS = 60

SEA_MAP_IMAGE = pygame.image.load(
    os.path.join('assets', 'map', 'tiled_sea.png'))


def create_gui_items() -> dict:
    """
      This method creates gui items used in screen.
    """
    
    start_button = Button(
        text='Start game!',
        pos_x=20,
        pos_y=20,
        width=200,
        height=40
    )

    gui_items = {
        'start_button': start_button
    }

    return gui_items


def create_ships_sprites() -> pygame.sprite.Group:
    """
      This method creates all ship sprites and add them to
      an sprite group.
    """
    
    ships_group = pygame.sprite.Group()
    new_carrier = Carrier(35, 45)
    
    ships_group.add(new_carrier)
    
    return ships_group


def draw_window(sprite_groups: dict, gui_items: dict) -> None:
    """
      This method draws everything to the main window.
    """

    # Draw background
    WIN.fill(BACKGROUND_COLOR)
    WIN.blit(SEA_MAP_IMAGE, (35, 45))

    # Draw GUI
    for _, gui_item in gui_items.items():
        gui_item.draw(WIN)

    # Draw sprite groups
    for _, sprite_group in sprite_groups.items():
        sprite_group.draw(WIN)

    pygame.display.update()


def main():
    # Handle sprite group painting dynamically
    ships_group = create_ships_sprites()
    sprite_groups = {}

    # Handling GUI elements painting dynamically
    gui_items = create_gui_items()

    # TODO: Create "Start" button to show up Ships to place
    # TODO: Create Ships options to place
    # https://stackoverflow.com/questions/19877900/tips-on-adding-creating-a-drop-down-selection-box-in-pygame
    # https://stackoverflow.com/questions/30751547/python-pygame-how-to-create-a-drag-and-drop-with-multiple-images
    # https://stackoverflow.com/questions/56984542/is-there-an-effiecient-way-of-making-a-function-to-drag-and-drop-multiple-pngs

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Force game loop to run at FPS limit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(sprite_groups, gui_items)

        if gui_items['start_button'].click():
            print('clicked')

    pygame.quit()


if __name__ == '__main__':
    main()
