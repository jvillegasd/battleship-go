import sys
import pygame
from typing import Tuple

# Import GUI items
from gui.grid import Grid
from gui.map_widget import MapWidget

# Import animations
from sprites.animations.fire import Fire
from sprites.animations.explosion import Explosion


class Battle:
    """ This class manages Battle stage. """

    def __init__(self) -> None:
        self.states = {
            'game_finished': False,
            'winner_name': None,
            'maps_ships_loaded': False
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

            if self.states['maps_ships_loaded']:
                self.map_widget.handle_button_tabs_events()
                
                if self.__ally_tab_selected():
                    self.gui_items['ships']['enabled'] = True
                else:
                    self.gui_items['ships']['enabled'] = False

                if not self.map_widget.ally_map_selected:
                    self.attack_enemy_ship(
                        event, self.map_widget.enemy_map, self.ships)

                self.__handle_attack_animation()

        return self.states

    def load_maps_and_ships(self, maps: MapWidget, ships: list) -> None:
        """ This function loads into GUI map widget and ships """

        self.map_widget = maps
        self.ships = ships

        self.gui_items['tabs']['item'] = self.map_widget
        self.gui_items['tabs']['enabled'] = True

        self.gui_items['ships']['item'] = self.ships
        self.gui_items['ships']['enabled'] = True

        self.states['maps_ships_loaded'] = True

    def attack_enemy_ship(
            self,
            event: pygame.event.Event,
            grid: Grid,
            ships: list) -> Tuple[bool, str]:
        """
          This function handles required mouse events to
          attack enemy ship.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            attacked, ship_name = grid.attack_tile(event.pos)
            if attacked:
                explosion = Explosion(
                    pos_x=event.pos[0],
                    pos_y=event.pos[1],
                    stop_after_finish=True
                )

                centered_position = grid.center_position(event.pos)
                explosion.center_animation_from_position(centered_position)
                self.gui_items['enemy_fire']['item'].append(explosion)

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        gui_items = {
            'tabs': {
                'enabled': False,
                'item': None
            },
            'ships': {
                'enabled': False,
                'item': None
            },
            'ally_fire': {
                'enabled': True,
                'item': []
            },
            'enemy_fire': {
                'enabled': True,
                'item': []
            }
        }

        return gui_items

    def __ally_tab_selected(self) -> bool:
        """ This function checks if ally tab is selected. """
        return (self.gui_items['tabs']['enabled'] and
                self.gui_items['tabs']['item'].ally_map_selected)

    def __handle_attack_animation(self) -> None:
        """
          This function iterates over attack animation lists
          to find which explossion animation is finished
          so, they can be replaced by fire animation.
        """

        for map_fire in ['ally_fire', 'enemy_fire']:
            for i, animation in enumerate(self.gui_items[map_fire]['item']):
                if type(animation) == Explosion and animation.animation_finished():
                    new_fire = Fire(
                        pos_x=animation.pos_x,
                        pos_y=animation.pos_y
                    )
                    new_fire.center_animation_from_position(
                        animation.rect.center)
                    self.gui_items[map_fire]['item'][i] = new_fire

        # Enable animation for current tab
        if self.gui_items['tabs']['item'].ally_map_selected:
            self.gui_items['ally_fire']['enabled'] = True
            self.gui_items['enemy_fire']['enabled'] = False
        else:
            self.gui_items['ally_fire']['enabled'] = False
            self.gui_items['enemy_fire']['enabled'] = True
