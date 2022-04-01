import pygame
from typing import Tuple, List

# Import GUI items
from gui.grid import Grid
from gui.button import Button
from gui.map_tab import MapTab

# Import sprites
from sprites.rescue_ship import RescueShip
from sprites.battleship import Battleship
from sprites.cruiser import Cruiser
from sprites.destroyer import Destroyer
from sprites.submarine import Submarine

# Import animations
from sprites.animations.fire import Fire
from sprites.animations.explosion import Explosion


WIDTH, HEIGHT = 940, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')

# Color name: Little Greene French Grey Pale
BACKGROUND_COLOR = (231, 231, 219)

FPS = 30
GUI_ITEMS = {}


# ------------------------------------------------------------
# GUI related functions
# ------------------------------------------------------------


def create_gui_items() -> dict:
    """
      This function creates gui items used in screen.
    """

    start_button = Button(
        text='Start',
        pos_x=655,
        pos_y=200,
        width=70,
        height=40
    )
    lock_ships = Button(
        text='Lock ships',
        pos_x=136,
        pos_y=400,
        width=110,
        height=40
    )
    grid = Grid(
        pos_x=35,
        pos_y=45
    )
    map_gui = MapTab(
        pos_x=500,
        pos_y=100
    )

    gui_items = {
        'start_button': {
            'enabled': True,
            'item': start_button
        },
        'lock_ships': {
            'enabled': False,
            'item': lock_ships
        },
        'map': {
            'enabled': True,
            'item': grid
        },
        'tabs': {
            'enabled': True,
            'item': map_gui
        }
    }

    return gui_items


def create_ships() -> Tuple[list, list]:
    """
      This function creates all ships and return two list
      refering to them and their rects.
    """

    new_battleship = Battleship(76, 157)

    new_carrier = RescueShip(51, 147)
    new_cruiser = Cruiser(160, 149)
    new_destroyer = Destroyer(257, 147)
    new_submarine = Submarine(282, 158)

    ships = [
        new_carrier,
        new_battleship,
        new_cruiser,
        new_destroyer,
        new_submarine
    ]

    ships_rect = [
        new_carrier.collision_rect,
        new_battleship.collision_rect,
        new_cruiser.collision_rect,
        new_destroyer.collision_rect,
        new_submarine.collision_rect
    ]

    return ships, ships_rect


def draw_window() -> None:
    """
      This function draws everything to the main window.
    """

    # Draw background
    WIN.fill(BACKGROUND_COLOR)

    # Draw GUI items
    for _, gui_item in GUI_ITEMS.items():
        if not gui_item['enabled']:
            continue

        if type(gui_item['item']) == list:
            for item in gui_item['item']:
                item.draw(WIN)
        else:
            gui_item['item'].draw(WIN)

    # Draw selected tile if grid is loaded
    if 'map' in GUI_ITEMS:
        GUI_ITEMS['map']['item'].draw_selected_tile(WIN)

    pygame.display.update()


def handle_buttom_click(gui_btn: dict) -> bool:
    return gui_btn['enabled'] and gui_btn['item'].click()


# ------------------------------------------------------------
# Ship location stage functions
# ------------------------------------------------------------


def drag_and_drop_ship(
        event,
        grid: Grid,
        ships: list,
        ships_rect: list,
        selected_ship: int) -> Tuple[int, bool]:
    """
      This function handles required mouse events to drag and
      drop ships over grid.
    """

    dragging = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_rect = pygame.Rect(event.pos, (1, 1))
        selected_ship = mouse_rect.collidelist(ships_rect)

    if event.type == pygame.MOUSEMOTION:
        if event.buttons[0]:
            dragging = True
            if 0 <= selected_ship < len(ships):
                ships[selected_ship].move_ship(event.rel, grid, ships_rect)
                ships_rect[selected_ship] = ships[selected_ship].rect

    if event.type == pygame.MOUSEBUTTONUP:
        if 0 <= selected_ship < len(ships):
            ships[selected_ship].dragged_ship_position(grid)
            ships_rect[selected_ship] = ships[selected_ship].rect

    return selected_ship, dragging


def enable_ship_rotation(
        grid: Grid,
        ships: list,
        ships_rect: List[pygame.Rect],
        selected_ship: int,
        dragging: bool) -> None:
    """
      This function enables rotation button to selected ship.
    """

    global GUI_ITEMS

    # Check if selected ship rotation buttom can be drawed
    if 0 <= selected_ship < len(ships) and not dragging:
        # Add rotation button of selected ship to GUI
        GUI_ITEMS['rotate_ship'] = {
            'enabled': True,
            'item': ships[selected_ship].rotate_btn
        }

        if handle_buttom_click(GUI_ITEMS['rotate_ship']):
            ships[selected_ship].rotate_ship(grid, ships_rect)
            ships_rect[selected_ship] = ships[selected_ship].rect
    elif 'rotate_ship' in GUI_ITEMS:
        GUI_ITEMS['rotate_ship']['enabled'] = False


def ship_location_stage_events(
        event,
        ships: list,
        ships_rect: List[pygame.Rect],
        selected_ship: int) -> int:
    """
      This function handles pygame events related to ship location stage.
    """

    selected_ship, dragging = drag_and_drop_ship(
        event, GUI_ITEMS['map']['item'], ships, ships_rect, selected_ship)

    enable_ship_rotation(
        GUI_ITEMS['map']['item'], ships, ships_rect, selected_ship, dragging)

    return selected_ship


# ------------------------------------------------------------
# Battle stage functions
# ------------------------------------------------------------


def handle_attack_animation():
    """
      This function iterates over attack animation list
      to find which explossion animation is finished
      so, they can be replaced by fire animation.
    """

    for i, animation in enumerate(GUI_ITEMS['fire']['item']):
        if type(animation) == Explosion and animation.animation_finished():
            new_fire = Fire(
                pos_x=animation.pos_x,
                pos_y=animation.pos_y
            )
            new_fire.center_animation_from_position(animation.rect.center)
            GUI_ITEMS['fire']['item'][i] = new_fire


def attack_enemy_ship(event, grid: Grid, ships: list) -> Tuple[bool, str]:
    """
      This function handles required mouse events to
      attack enemy ship.
    """

    global GUI_ITEMS

    if event.type == pygame.MOUSEBUTTONDOWN:
        attacked, ship_name = grid.attack_enemy(event.pos)

        if attacked:

            explosion = Explosion(
                pos_x=event.pos[0],
                pos_y=event.pos[1],
                stop_after_finish=True
            )

            centered_position = grid.center_position(event.pos)
            explosion.center_animation_from_position(centered_position)
            GUI_ITEMS['fire']['item'].append(explosion)


def battle_stage_events(event, ships: list):
    """
      This function handles pygame events related to battle stage.
    """

    attack_enemy_ship(event, GUI_ITEMS['map']['item'], ships)

    handle_attack_animation()


# ------------------------------------------------------------
# Main loop function
# ------------------------------------------------------------


def main():
    global GUI_ITEMS

    # TODO: Create UI (For maps (ally-enemy): Create tab system, chat)
    # TODO: Calculate life of ships (attacking) and show bubble with info
    # TODO: Create client-server networking for multiplayer
    # TODO: Reset battle buttom

    # Handle game state variables
    game_started = False
    ships_locked = False
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
                # Ships location stage
                if not ships_locked:
                    selected_ship = ship_location_stage_events(
                        event, ships, ships_rect, selected_ship)

                # Battle stage
                if ships_locked:
                    battle_stage_events(event, ships)

        if game_started:
            if not ships_locked:
                if handle_buttom_click(GUI_ITEMS['lock_ships']):
                    ships_locked = True
                    GUI_ITEMS['fire'] = {
                        'enabled': True,
                        'item': []
                    }
                    GUI_ITEMS['lock_ships']['enabled'] = False
                    GUI_ITEMS['map']['item'].locate_ships_into_game_grid(ships)
        else:
            if handle_buttom_click(GUI_ITEMS['start_button']):
                game_started = True
                GUI_ITEMS['ships'] = {
                    'enabled': True,
                    'item': ships
                }
                GUI_ITEMS['lock_ships']['enabled'] = True
                GUI_ITEMS['start_button']['enabled'] = False

        draw_window()

    pygame.quit()


if __name__ == '__main__':
    main()
