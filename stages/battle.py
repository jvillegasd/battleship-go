import sys
import pygame
from typing import List, Union

# Import client
from networking.client import Client

# Import GUI items
from gui.grid import Grid
from gui.label import Label
from gui.dev_sign import DevSign
from gui.map_widget import MapWidget

# Import animations
from sprites.animations.fire import Fire
from sprites.animations.explosion import Explosion


class Battle:
    """ This class manages Battle stage. """

    def __init__(self) -> None:
        self.states = {
            'client': None,
            'winner_name': None,
            'game_finished': False,
            'maps_ships_loaded': False,
            'last_selected_ship': -1
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

    def load_client(self, client: Client) -> None:
        """ This function loads connected client to current stage. """
        self.states['client'] = client

    def is_client_disconnected(self) -> bool:
        """ This function checks if client is disconnected. """
        return ((self.states['client'] and self.states['client'].is_disconnected)
                or not self.states['client'])

    def attack_enemy_ship(self, event: pygame.event.Event, grid: Grid) -> None:
        """
          This function handles required mouse events to
          attack enemy ship.
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            tile_pos = grid.translate_position(event.pos)
            if grid.is_valid_position(tile_pos):
                ship_name = self.states['client'].attack_enemy_tile(tile_pos)

                if ship_name:
                    explosion = Explosion(
                        pos_x=event.pos[0],
                        pos_y=event.pos[1],
                        stop_after_finish=True
                    )

                    grid.game_grid[tile_pos[0]][tile_pos[1]] = 'X'

                    centered_pos = grid.center_position(event.pos)
                    explosion.center_animation_from_position(centered_pos)
                    self.gui_items['enemy_fire']['item'].append(explosion)

    def receive_enemy_attack(
            self,
            grid: Grid,
            ships: list) -> None:
        """ This function check if enemy attack hits a ship """

        response = self.states['client'].get_game_data()
        enemy_data = next(
            (
                value
                for key, value in response.items()
                if key != self.states['client'].client_name), None)
        if (
            enemy_data['attacked_tile']['ship_name']
            and enemy_data['attacked_tile']['ship_name'] != 'X'
        ):
            position = enemy_data['attacked_tile']['position']
            if grid.game_grid[position[1]][position[0]] != 'X':
                rescaled_pos = grid.upscale_position(position)
                rescaled_pos = grid.center_position(rescaled_pos)

                explosion = Explosion(
                    pos_x=rescaled_pos[0],
                    pos_y=rescaled_pos[1],
                    stop_after_finish=True
                )

                attacked_ship = next(
                    (
                        ship
                        for ship in ships
                        if ship.name == enemy_data['attacked_tile']['ship_name']), None)
                attacked_ship.get_attacked()
                grid.game_grid[position[1]][position[0]] = 'X'

                if attacked_ship.get_ship_life() == 0:
                    self.states['client'].ship_sinked()

                explosion.center_animation_from_position(rescaled_pos)
                self.gui_items['ally_fire']['item'].append(explosion)

    def check_player_turn(self, is_my_turn: bool) -> None:
        """ This function shows the current player turn. """

        label_offset = (0, 0)

        if is_my_turn:
            label_offset = (50, 0)
            self.gui_items['turn_label']['item'].change_text('My turn!')
        else:
            label_offset = (15, 0)
            self.gui_items['turn_label']['item'].change_text(
                'Waiting for enemy turn...')

        self.gui_items['turn_label']['item'].move_label(label_offset)

    def process_events(self) -> dict:
        """
          This function handles pygame events related
          to current stage.
        """

        if self.is_client_disconnected():
            pygame.quit()
            sys.exit()

        is_my_turn = self.states['client'].is_my_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.states['client']:
                    self.states['client'].disconnect()

                pygame.quit()
                sys.exit()

            if self.states['maps_ships_loaded']:
                if self.__ally_tab_selected():
                    self.gui_items['ships']['enabled'] = True
                else:
                    self.gui_items['ships']['enabled'] = False
                    if is_my_turn:
                        self.attack_enemy_ship(
                            event, self.map_widget.enemy_map)

        self.check_player_turn(is_my_turn)

        if self.states['maps_ships_loaded']:
            self.receive_enemy_attack(
                self.map_widget.ally_map, self.ships)
            self.states['last_selected_ship'] = self.__show_ship_life_status()
            self.__handle_attack_animation()
            self.map_widget.handle_button_tabs_events()

        winner_name = self.states['client'].get_winner()
        if winner_name:
            self.states['winner_name'] = winner_name
            self.states['game_finished'] = True

        return self.states

    def load_maps_and_ships(
            self,
            maps: MapWidget,
            ships: list,
            ships_rect: List[pygame.Rect]) -> None:
        """ This function loads into GUI map widget and ships """

        self.map_widget = maps
        self.ships = ships
        self.ships_rect = ships_rect

        self.gui_items['tabs']['item'] = self.map_widget
        self.gui_items['tabs']['enabled'] = True

        self.gui_items['ships']['item'] = self.ships
        self.gui_items['ships']['enabled'] = True

        self.states['maps_ships_loaded'] = True

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        sign = DevSign(pos_x=325, pos_y=475)
        turn_label = Label(pos_x=130, pos_y=430,
                           text='Waiting for enemy turn...')

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
            },
            'dev_sign': {
                'enabled': True,
                'item': sign
            },
            'turn_label': {
                'enabled': True,
                'item': turn_label
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

    def __show_ship_life_status(self) -> int:
        """ This function show ship current life when it is hovered. """

        mouse_pos = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_pos, (1, 1))

        selected_ship = mouse_rect.collidelist(self.ships_rect)
        last_selected_ship = self.states['last_selected_ship']

        if self.__valid_ship_index(selected_ship):
            self.ships[selected_ship].can_draw_bubble = True

            if last_selected_ship != selected_ship:
                self.ships[last_selected_ship].can_draw_bubble = False
        elif self.__valid_ship_index(last_selected_ship):
            self.ships[last_selected_ship].can_draw_bubble = False

        return selected_ship

    def __valid_ship_index(self, selected_ship: int) -> bool:
        """ This function checks if selected_ship is a valid index """
        return 0 <= selected_ship < len(self.ships)
