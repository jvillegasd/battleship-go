import sys
import pygame

# Import client
from networking.client import Client

# Import GUI items
from gui.card import Card
from gui.label import Label
from gui.button import Button
from gui.dev_sign import DevSign


class Podium:
    """ This class manges Podium stage. """

    def __init__(self) -> None:
        self.states = {
            'client': None,
            'winner_name': '',
            'reset_game': False
        }
        self.gui_items = self.__load_gui_items()

        # Color name: Little Greene French Grey Pale
        self.background_color = (231, 231, 219)

    def handle_buttom_click(self, gui_btn: dict) -> bool:
        """ This function handles button click event """
        return gui_btn['enabled'] and gui_btn['item'].click()

    def draw(self, window: pygame.display) -> dict:
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

        pygame.display.update()

    def load_client(self, client: Client) -> None:
        """ This function loads connected client to current stage. """
        self.states['client'] = client

    def load_winner_name(self, winner_name: str) -> None:
        """ This function loads winner name. """

        self.states['winner_name'] = winner_name
        self.gui_items['winner_label']['item'].change_text(
            f'The winner is: {winner_name}')

    def is_client_disconnected(self) -> bool:
        """ This function checks if client is disconnected. """
        return ((self.states['client'] and self.states['client'].is_disconnected)
                or not self.states['client'])

    def is_game_reseted(self) -> bool:
        """ This function checks if game is reseted. """

        if self.states['client']:
            game_status = self.states['client'].get_game_status()
            return game_status == 'ship_lock'

        return False

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

        if self.handle_buttom_click(self.gui_items['reset_button']):
            self.states['client'].reset_game()
            self.states['reset_game'] = True

        if self.is_game_reseted():
            self.states['reset_game'] = True

        return self.states

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        sign = DevSign(pos_x=325, pos_y=475)
        card = Card(
            pos_x=100,
            pos_y=140,
            width=300,
            height=200
        )
        winner_label = Label(pos_x=170, pos_y=203, text='The winner is: XXXXX')
        reset_button = Button(
            text='New game',
            pos_x=187,
            pos_y=260,
            width=120,
            height=40
        )

        gui_items = {
            'dev_sign': {
                'enabled': True,
                'item': sign
            },
            'card': {
                'enabled': True,
                'item': card
            },
            'winner_label': {
                'enabled': True,
                'item': winner_label
            },
            'reset_button': {
                'enabled': True,
                'item': reset_button
            }
        }

        return gui_items
