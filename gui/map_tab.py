import pygame

from gui.grid import Grid
from gui.button import Button


class MapTab:

    def __init__(self, pos_x: float, pos_y: float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.width = 350
        self.height = 350
        self.btn_width = 90
        self.btn_height = 30

        self.main_rect = pygame.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.main_rect_color = (204, 230, 244)
        self.main_rect_border_radius = 12
        
        self.ally_map_selected = True
        self.selected_tab_color = '#72788D'
        self.unselected_tab_color = '#AEC301'

        self.ally_tab_btn = Button(
            text="Your map",
            pos_x=self.pos_x,
            pos_y=self.pos_y,
            width=self.btn_width,
            height=self.btn_height,
            btn_color=self.selected_tab_color,
            btn_hover_color=self.selected_tab_color,
            elevation=0,
            border_radius=0
        )  
        self.enemy_tab_btn = Button(
            text="Enemy map",
            pos_x=self.pos_x + self.btn_width,
            pos_y=self.pos_y,
            width=self.btn_width,
            height=self.btn_height,
            btn_color=self.unselected_tab_color,
            btn_hover_color=self.unselected_tab_color,
            elevation=0,
            border_radius=0
        )

    def draw(self, window: pygame.display) -> None:
        pygame.draw.rect(window, self.main_rect_color, self.main_rect,
                         border_radius=self.main_rect_border_radius)
        
        self.ally_tab_btn.draw(window)
        self.enemy_tab_btn.draw(window)
        
        self.__handle_button_tabs_events()
    
    
    def __handle_button_tabs_events(self) -> None:
        if self.ally_tab_btn.click():
            self.ally_map_selected = True
            print('tab 1', self.ally_map_selected)
            self.ally_tab_btn.change_top_colors(self.selected_tab_color)
            self.enemy_tab_btn.change_top_colors(self.unselected_tab_color)
        if self.enemy_tab_btn.click():
            self.ally_map_selected = False
            print('tab 2', self.ally_map_selected)
            self.ally_tab_btn.change_top_colors(self.unselected_tab_color)
            self.enemy_tab_btn.change_top_colors(self.selected_tab_color)
