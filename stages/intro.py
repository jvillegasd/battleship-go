import pygame
import sys

from gui.button import Button


class Intro:
    """ This class manages Intro stage game state. """
    
    def __init__(self) -> None:
        self.states = {
            'game_started': False
        }
        self.gui_items = self.__load_gui_items()

        # Color name: Little Greene French Grey Pale
        self.background_color = (231, 231, 219)

    def __load_gui_items(self) -> dict:
        """
          This function creates and loads gui items
          used in stage.
        """
        
        start_button = Button(
            text='Start game',
            pos_x=190,
            pos_y=220,
            width=120,
            height=40
        )

        gui_items = {
            'start_button': {
                'enabled': True,
                'item': start_button
            }
        }

        return gui_items

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

        if self.handle_buttom_click(self.gui_items['start_button']):
            self.states['game_started'] = True

        return self.states
