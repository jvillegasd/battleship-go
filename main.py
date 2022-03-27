import pygame
from typing import Tuple

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
GUI_ITEMS = {}


def create_gui_items() -> dict:
    """
      This method creates gui items used in screen.
    """

    start_button = Button(
        text='Start game!',
        pos_x=95,
        pos_y=400,
        width=130,
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


def create_ships() -> Tuple[list, list]:
    """
      This method creates all ships and return two list
      refering to them and their rects.
    """

    new_battleship = Battleship(75, 150)

    new_carrier = RescueShip(43, 150)
    new_cruiser = Cruiser(155, 150)
    new_destroyer = Destroyer(250, 150)
    new_submarine = Submarine(280, 150)

    ships = [
        new_carrier,
        new_battleship,
        new_cruiser,
        new_destroyer,
        new_submarine
    ]

    ships_rect = [
        new_carrier.rect,
        new_battleship.rect,
        new_cruiser.rect,
        new_destroyer.rect,
        new_submarine.rect
    ]

    return ships, ships_rect


def draw_window() -> None:
    """
      This method draws everything to the main window.
    """

    # Draw background
    WIN.fill(BACKGROUND_COLOR)

    # Draw GUI items
    for _, gui_item in GUI_ITEMS.items():
        if type(gui_item) == list:
            for item in gui_item:
                item.draw(WIN)
        else:
            gui_item.draw(WIN)

    # Draw selected tile if grid is loaded
    if 'map' in GUI_ITEMS:
        GUI_ITEMS['map'].draw_selected_tile(WIN)

    pygame.display.update()


def drag_and_drop_ships(
        event,
        grid: Grid,
        ships: list,
        ships_rect: list,
        selected_ship: int) -> int:
    """
      This method handles mouse events when ships can be moved
      from grid.
    """

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_rect = pygame.Rect(event.pos, (1, 1))
        selected_ship = mouse_rect.collidelist(ships_rect)

    if event.type == pygame.MOUSEMOTION:
        if event.buttons[0]:
            if 0 <= selected_ship < len(ships):
                ships[selected_ship].move_ship(event.rel, grid)
                ships_rect[selected_ship] = ships[selected_ship].rect

    if event.type == pygame.MOUSEBUTTONUP:
        if 0 <= selected_ship < len(ships):
            ships[selected_ship].dragged_ship_position(grid)
            ships_rect[selected_ship] = ships[selected_ship].rect

    return selected_ship


def enable_ship_rotation(
        grid: Grid,
        ships: list,
        ships_rect: list,
        selected_ship: int) -> None:

    """

    """
    
    # Add rotation button of selected ship to GUI
    if not 'rotate_ship' in GUI_ITEMS:
      GUI_ITEMS['rotate_ship'] = ships[selected_ship].rotate_btn
    
    if ships[selected_ship].rotate_btn.click():
        ships[selected_ship].rotate_ship(grid)
        ships_rect[selected_ship] = ships[selected_ship].rect


def main():
    global GUI_ITEMS

    # Handle game state variables
    game_started = False
    selected_ship = -1

    # Create ships and handle selected
    ships, ships_rect = create_ships()

    # Handling GUI elements painting dynamically
    GUI_ITEMS = create_gui_items()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Force game loop to run at FPS limit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game_started:
                selected_ship = drag_and_drop_ships(
                    event, GUI_ITEMS['map'], ships, ships_rect, selected_ship)

                if 0 <= selected_ship < len(ships):
                    enable_ship_rotation(
                        GUI_ITEMS['map'], ships, ships_rect, selected_ship)
                else:
                  GUI_ITEMS.pop('rotate_ship', None)

        if GUI_ITEMS['start_button'].click():
            if not game_started:
                game_started = True
                GUI_ITEMS['ships'] = ships

        draw_window()

    pygame.quit()


if __name__ == '__main__':
    main()
