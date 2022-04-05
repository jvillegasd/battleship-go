import sys
import pygame
from typing import Tuple, List

# Import GUI items
from gui.grid import Grid
from gui.button import Button
from gui.map_widget import MapWidget

# Import sprites
from sprites.rescue_ship import RescueShip
from sprites.battleship import Battleship
from sprites.cruiser import Cruiser
from sprites.destroyer import Destroyer
from sprites.submarine import Submarine


class ShipLocation:
    """ This class manages Ship location stage. """

    def __init__(self) -> None:
        self.states = {
            'selected_ship': -1,
            'ship_locked': False
        }

        self.map_widget = MapWidget(pos_x=73, pos_y=25)
        self.ships, self.ships_rect = self.__create_ships()
        self.gui_items = self.__load_gui_items()

        # Color name: Little Greene French Grey Pale
        self.background_color = (231, 231, 219)

    def handle_buttom_click(self, gui_btn: dict) -> bool:
        """ This function handles button click event """
        return gui_btn['enabled'] and gui_btn['item'].click()

    def draw(self, window: pygame.display) -> None:
        """ This function draws gui items on window. """

        # Draw background
        window.fill(self.background_color)

        # Draw GUI items
        for _, gui_item in self.gui_items.items():
            if not gui_item['enabled']:
                continue

            if type(gui_item['item']) == list:
                for item in gui_item['item']:
                    item.draw(window)
            else:
                gui_item['item'].draw(window)

        # Draw selected tile for current tab
        if self.gui_items['tabs']['enabled']:
            if self.map_widget.ally_map_selected:
                self.map_widget.ally_map.draw_selected_tile(window)
            else:
                self.map_widget.enemy_map.draw_selected_tile(window)

        pygame.display.update()

    def process_events(self) -> dict:
        """
          This function handles pygame events related
          to current stage.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.__ally_tab_selected():
                self.gui_items['ships']['enabled'] = True

                self.states['selected_ship'], dragging = self.__drag_and_drop_ship(
                    event, self.map_widget.ally_map, self.states['selected_ship'])

                self.__enable_ship_rotation(
                    self.map_widget.ally_map, self.states['selected_ship'], dragging)
            else:
                self.gui_items['ships']['enabled'] = False

        if self.handle_buttom_click(self.gui_items['lock_ships']):
            self.states['ship_locked'] = True
            self.ships = self.map_widget.ally_map.locate_ships_into_game_grid(
                self.ships)

        return self.states

    def get_maps_and_ships(self) -> Tuple[MapWidget, list, List[pygame.Rect]]:
        """ This function returns map widget and ships """
        return self.map_widget, self.ships, self.ships_rect

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        lock_ships = Button(
            text='Lock ships',
            pos_x=190,
            pos_y=430,
            width=110,
            height=40
        )

        gui_items = {
            'lock_ships': {
                'enabled': True,
                'item': lock_ships
            },
            'tabs': {
                'enabled': True,
                'item': self.map_widget
            },
            'ships': {
                'enabled': True,
                'item': self.ships
            }
        }

        return gui_items

    def __ally_tab_selected(self) -> bool:
        """ This function checks if ally tab is selected. """
        return (self.gui_items['tabs']['enabled'] and
                self.gui_items['tabs']['item'].ally_map_selected)

    def __drag_and_drop_ship(
            self,
            event: pygame.event.Event,
            grid: Grid,
            selected_ship: int) -> Tuple[int, bool]:
        """
          This function handles required mouse events to drag and
          drop ships over grid.
        """

        dragging = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_rect = pygame.Rect(event.pos, (1, 1))
            selected_ship = mouse_rect.collidelist(self.ships_rect)

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                dragging = True
                if 0 <= selected_ship < len(self.ships):
                    self.ships[selected_ship].move_ship(
                        event.rel, grid, self.ships_rect)
                    self.ships_rect[selected_ship] = self.ships[selected_ship].rect

        if event.type == pygame.MOUSEBUTTONUP:
            if 0 <= selected_ship < len(self.ships):
                self.ships[selected_ship].dragged_ship_position(grid)
                self.ships_rect[selected_ship] = self.ships[selected_ship].rect

        return selected_ship, dragging

    def __enable_ship_rotation(
            self,
            grid: Grid,
            selected_ship: int,
            dragging: bool) -> None:
        """ This function enables rotation button to selected ship. """

        # Check if selected ship rotation buttom can be drawed
        if 0 <= selected_ship < len(self.ships) and not dragging:
            # Add rotation button of selected ship to GUI
            self.gui_items['rotate_ship'] = {
                'enabled': True,
                'item': self.ships[selected_ship].rotate_btn
            }

            if self.handle_buttom_click(self.gui_items['rotate_ship']):
                self.ships[selected_ship].rotate_ship(grid, self.ships_rect)
                self.ships_rect[selected_ship] = self.ships[selected_ship].rect
        elif 'rotate_ship' in self.gui_items:
            self.gui_items['rotate_ship']['enabled'] = False

    def __create_ships(self) -> Tuple[list, list]:
        """
          This function creates all ships and return two list
          refering to them and their rects.
        """

        new_rescue_ship = RescueShip(88, 266)
        new_battleship = Battleship(129, 164)
        new_cruiser = Cruiser(197, 156)
        new_destroyer = Destroyer(262, 154)
        new_submarine = Submarine(319, 165)

        ships = [
            new_rescue_ship,
            new_battleship,
            new_cruiser,
            new_destroyer,
            new_submarine
        ]

        ships_rect = [
            new_rescue_ship.collision_rect,
            new_battleship.collision_rect,
            new_cruiser.collision_rect,
            new_destroyer.collision_rect,
            new_submarine.collision_rect
        ]

        return ships, ships_rect
