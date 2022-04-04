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
        
        self.gui_items['tabs']['item'] = maps
        self.gui_items['tabs']['enabled'] = True
        
        self.gui_items['ships']['item'] = ships
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
                'item': []
            },
            'tabs': {
                'enabled': False,
                'item': None
            }
        }

        return gui_items
