import sys
import pygame
from typing import Tuple

# Import GUI items
from gui.grid import Grid
from gui.map_widget import MapWidget


class Battle:
    """ This class manages Battle stage. """

    def __init__(self) -> None:
        self.states = {
            'game_finished': False,
            'winner_name': None
        }

        self.gui_items = self.__load_gui_items()
        
        # Color name: Little Greene French Grey Pale
        self.background_color = (231, 231, 219)

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

        return self.states

    def load_maps_and_ships(self, maps: MapWidget, ships: list) -> None:
        """ This function loads into GUI map widget and ships """

        self.map_widget = maps
        self.ships = ships
        
        self.gui_items['tabs']['item'] = self.map_widget
        self.gui_items['tabs']['enabled'] = True

        self.gui_items['ships']['item'] = self.ships
        self.gui_items['ships']['enabled'] = True

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        gui_items = {
            'ally_fire': {
                'enabled': True,
                'item': []
            },
            'enemy_fire': {
                'enabled': True,
                'item': []
            },
            'ships': {
                'enabled': False,
                'item': None
            },
            'tabs': {
                'enabled': False,
                'item': None
            }
        }

        return gui_items
