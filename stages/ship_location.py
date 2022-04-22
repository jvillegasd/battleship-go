from http.client import responses
import sys
import pygame
from typing import Tuple, List

# Import client
from networking.client import Client

# Import GUI items
from gui.grid import Grid
from gui.label import Label
from gui.button import Button
from gui.dev_sign import DevSign
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
            'client': None,
            'ship_locked': False,
            'last_selected_ship': -1
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

    def load_client(self, client: Client) -> None:
        """ This function loads connected client to current stage. """
        self.states['client'] = client

    def is_client_disconnected(self) -> bool:
        """ This function checks if client is disconnected. """
        return ((self.states['client'] and self.states['client'].is_disconnected)
                or not self.states['client'])

    def is_game_started(self) -> bool:
        """
          This function fetch game status from server
          and checks if all clients locked their ship.
        """

        if self.states['client']:
            game_status = self.states['client'].get_game_status()
            return game_status == 'battle'

        return False

    def lock_ships_position(self) -> None:
        """ This function notifies to server that a client locked ships. """

        if self.states['client']:
            self.ships = self.map_widget.ally_map.locate_ships_into_game_grid(
                self.ships)
            self.states['client'].lock_ships_and_send_game_grid(
                self.map_widget.ally_map.game_grid)

            self.gui_items['conn_label']['enabled'] = True
            self.gui_items['lock_ships']['enabled'] = False

    def process_events(self) -> dict:
        """
          This function handles pygame events related
          to current stage.
        """

        if self.is_client_disconnected():
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.states['client']:
                    self.states['client'].disconnect()

                pygame.quit()
                sys.exit()

            if self.__ally_tab_selected():
                self.gui_items['ships']['enabled'] = True
                selected_ship = self.states['last_selected_ship']

                selected_ship, dragging = self.__drag_and_drop_ship(
                    event, self.map_widget.ally_map, selected_ship)

                self.__enable_ship_rotation(
                    self.map_widget.ally_map, selected_ship, dragging)

                self.states['last_selected_ship'] = selected_ship
            else:
                self.gui_items['ships']['enabled'] = False

        self.map_widget.handle_button_tabs_events()
        if self.handle_buttom_click(self.gui_items['lock_ships']):
            self.lock_ships_position()

        if self.is_game_started():
            self.states['ship_locked'] = True

        return self.states

    def get_maps_and_ships(self) -> Tuple[MapWidget, list, List[pygame.Rect]]:
        """ This function returns map widget and ships """
        return self.map_widget, self.ships, self.ships_rect

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        sign = DevSign(pos_x=325, pos_y=475)
        lock_ships = Button(
            text='Lock ships',
            pos_x=190,
            pos_y=430,
            width=110,
            height=40
        )
        conn_label = Label(pos_x=130, pos_y=430,
                           text='Waiting for confirmation...')

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
            },
            'dev_sign': {
                'enabled': True,
                'item': sign
            },
            'conn_label': {
                'enabled': False,
                'item': conn_label
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
                if self.__valid_ship_index(selected_ship):
                    self.ships[selected_ship].move_ship(
                        event.rel, grid, self.ships_rect)
                    self.ships_rect[selected_ship] = self.ships[selected_ship].rect

        if event.type == pygame.MOUSEBUTTONUP:
            if self.__valid_ship_index(selected_ship):
                self.ships[selected_ship].dragged_ship_position(grid)
                self.ships_rect[selected_ship] = self.ships[selected_ship].rect

        return selected_ship, dragging

    def __enable_ship_rotation(
            self,
            grid: Grid,
            selected_ship: int,
            dragging: bool) -> None:
        """ This function enables rotation button to selected ship. """

        last_selected_ship = self.states['last_selected_ship']

        # Check if selected ship rotation button can be drawed
        if self.__valid_ship_index(selected_ship) and not dragging:
            self.ships[selected_ship].can_draw_button = True

            if last_selected_ship != selected_ship:
                self.ships[last_selected_ship].can_draw_button = False

            if self.ships[selected_ship].rotate_button_click():
                self.ships[selected_ship].rotate_ship(grid, self.ships_rect)
                self.ships_rect[selected_ship] = self.ships[selected_ship].rect
        elif self.__valid_ship_index(last_selected_ship):
            self.ships[last_selected_ship].can_draw_button = False

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

    def __valid_ship_index(self, selected_ship: int) -> bool:
        """ This function checks if selected_ship is a valid index """
        return 0 <= selected_ship < len(self.ships)
