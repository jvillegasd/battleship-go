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


def create_ships() -> Tuple[list, list]:
    """
      This method creates all ships and return two list
      refering to them and their rects.
    """

    ships = []
    ships_rect = []

    new_carrier = RescueShip(43, 313)
    new_battleship = Battleship(75, 150)
    new_cruiser = Cruiser(155, 300)
    new_destroyer = Destroyer(250, 300)
    new_submarine = Submarine(250, 154)

    ships.append(new_battleship)
    ships_rect.append(new_battleship.rect)

    return ships, ships_rect


def draw_window(gui_items: dict) -> None:
    """
      This method draws everything to the main window.
    """

    # Draw background
    WIN.fill(BACKGROUND_COLOR)

    # Draw GUI items
    for _, gui_item in gui_items.items():
        if type(gui_item) == list:
            for item in gui_item:
                item.draw(WIN)
        else:
            gui_item.draw(WIN)

    # Draw selected tile if grid is loaded
    if 'map' in gui_items:
        gui_items['map'].draw_selected_tile(WIN)

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


def main():
    # Handle game state variables
    game_started = False
    selected_ship = -1

    # Create ships and handle selected
    ships, ships_rect = create_ships()

    # Handling GUI elements painting dynamically
    gui_items = create_gui_items()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Force game loop to run at FPS limit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game_started:
                selected_ship = drag_and_drop_ships(
                    event, gui_items['map'], ships, ships_rect, selected_ship)

        if gui_items['start_button'].click():
            if not game_started:
                game_started = True
                gui_items['ships'] = ships

        draw_window(gui_items)

    pygame.quit()


if __name__ == '__main__':
    main()
