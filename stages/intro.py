import sys
import pygame

# Import GUI items
from gui.button import Button
from gui.dev_sign import DevSign
from gui.text_input import Input


class Intro:
    """ This class manages Intro stage. """

    def __init__(self) -> None:
        self.states = {
            'game_started': False
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

    def process_events(self) -> None:
        """
          This function handles pygame events related
          to current stage.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.gui_items['host_input']['enabled']:
                self.gui_items['host_input']['item'].handle_input_events(event)

        if self.handle_buttom_click(self.gui_items['start_button']):
            self.states['game_started'] = True

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
            pos_y=320,
            width=120,
            height=40
        )
        host_input = Input(pos_x=280, pos_y=150)
        port_input = Input(pos_x=280, pos_y=200)
        gui_items = {
            'start_button': {
                'enabled': True,
                'item': start_button
            },
            'dev_sign': {
                'enabled': True,
                'item': sign
            },
            'host_input': {
                'enabled': True,
                'item': host_input
            },
            'port_input': {
                'enabled': True,
                'item': port_input
            }
        }

        return gui_items
