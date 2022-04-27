import sys
import pygame

# Import client
from networking.client import Client

# Import GUI items
from gui.card import Card
from gui.label import Label
from gui.button import Button
from gui.text_input import Input
from gui.dev_sign import DevSign


class Intro:
    """ This class manages Intro stage. """

    def __init__(self) -> None:
        self.states = {
            'client': None,
            'players_connected': False
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

    def connect_to_server(self) -> None:
        """ This function creates a client to connect to game server. """

        label_offset = (0, 0)
        username = self.gui_items['username_input']['item'].get_text()
        host_address = self.gui_items['host_input']['item'].get_text()
        host_post = self.gui_items['port_input']['item'].get_text()

        client = Client(username, host_address, host_post)
        if client.connect_to_server():
            self.states['client'] = client
            
            label_offset = (5, 0)
            self.gui_items['conn_label']['item'].change_text(
                'Waiting for player...')
            self.gui_items['start_button']['enabled'] = False
        else:
            label_offset = (13, 0)
            self.gui_items['conn_label']['item'].change_text(
                'Connection error...')

        self.gui_items['conn_label']['item'].move_label(label_offset)
    
    def is_client_disconnected(self) -> bool:
        """ This function checks if client is disconnected. """
        return self.states['client'] and self.states['client'].is_disconnected
    
    def all_players_connected(self) -> bool:
        """
          This function fetchs game status from server
          and checks if all clients are ready.
        """
        
        if self.states['client']:
            game_status = self.states['client'].get_game_status()
            return game_status != 'lobby'
        
        return False
    
    def process_events(self) -> None:
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
            
            if self.gui_items['username_input']['enabled']:
                self.gui_items['username_input']['item'].handle_input_events(
                    event)

            if self.gui_items['host_input']['enabled']:
                self.gui_items['host_input']['item'].handle_input_events(event)

            if self.gui_items['port_input']['enabled']:
                self.gui_items['port_input']['item'].handle_input_events(event)

        if self.handle_buttom_click(self.gui_items['start_button']):
            self.connect_to_server()

        if self.all_players_connected():
            self.states['players_connected'] = True

        return self.states

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """

        sign = DevSign(pos_x=325, pos_y=475)
        start_button = Button(
            text='Start game',
            pos_x=187,
            pos_y=360,
            width=120,
            height=40
        )
        title_label = Label(
            pos_x=190,
            pos_y=80,
            text='Battleship',
            font_size=20
        )
        card = Card(
            pos_x=100,
            pos_y=140,
            width=300,
            height=300
        )
        conn_label = Label(pos_x=170, pos_y=163, text='Connect to a server')

        username_input = Input(pos_x=230, pos_y=210, width=120)
        username_label = Label(pos_x=150, pos_y=212, text='Username:')

        host_input = Input(pos_x=230, pos_y=257, width=120)
        host_label = Label(pos_x=150, pos_y=259, text='Host:')

        port_input = Input(pos_x=230, pos_y=300, width=120)
        port_label = Label(pos_x=150, pos_y=302, text='Port:')

        gui_items = {
            'dev_sign': {
                'enabled': True,
                'item': sign
            },
            'card': {
                'enabled': True,
                'item': card
            },
            'title_label': {
                'enabled': True,
                'item': title_label
            },
            'host_label': {
                'enabled': True,
                'item': host_label
            },
            'host_input': {
                'enabled': True,
                'item': host_input
            },
            'port_label': {
                'enabled': True,
                'item': port_label
            },
            'port_input': {
                'enabled': True,
                'item': port_input
            },
            'conn_label': {
                'enabled': True,
                'item': conn_label
            },
            'username_input': {
                'enabled': True,
                'item': username_input
            },
            'username_label': {
                'enabled': True,
                'item': username_label
            },
            'start_button': {
                'enabled': True,
                'item': start_button
            },
        }

        return gui_items
