import os
import pygame

from gui.button import Button
from sprites.rescue_ship import RescueShip
from sprites.battleship import Battleship
from sprites.cruiser import Cruiser
from sprites.destroyer import Destroyer
from sprites.plane import Plane
from sprites.submarine import Submarine
from gui.grid import Grid

WIDTH, HEIGHT = 940, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')

# Color name: Little Greene French Grey Pale
BACKGROUND_COLOR = (231, 231, 219)

FPS = 60


def create_gui_items() -> dict:
    """
      This method creates gui items used in screen.
    """
    
    start_button = Button(
        text='Start game!',
        pos_x=95,
        pos_y=400,
        width=200,
        height=40
    )
    grid = Grid(
      pos_x=35,
      pos_y=45
    )

    gui_items = {
        'start_button': start_button,
        'map': grid
    }

    return gui_items


def create_ships_sprites() -> pygame.sprite.Group:
    """
      This method creates all ship sprites and add them to
      an sprite group.
    """
    
    ships_group = pygame.sprite.Group()
    new_carrier = RescueShip(43, 313)
    new_battleship = Battleship(75, 150)
    new_cruiser = Cruiser(155, 300)
    new_destroyer = Destroyer(250, 300)
    new_submarine = Submarine(250, 154)
    
    ships_group.add(new_carrier)
    ships_group.add(new_battleship)
    ships_group.add(new_cruiser)
    ships_group.add(new_destroyer)
    ships_group.add(new_submarine)
    
    return ships_group


def draw_window(sprite_groups: dict, gui_items: dict) -> None:
    """
      This method draws everything to the main window.
    """

    # Draw background
    WIN.fill(BACKGROUND_COLOR)

    # Draw GUI
    for _, gui_item in gui_items.items():
        gui_item.draw(WIN)

    # Draw sprite groups
    for _, sprite_group in sprite_groups.items():
        sprite_group.draw(WIN)

    pygame.display.update()


def main():
    # Handle game state
    game_started = False
  
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
            if not game_started:
              game_started = True
              sprite_groups['ships'] = ships_group

    pygame.quit()


if __name__ == '__main__':
    main()
