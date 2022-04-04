import pygame

from gui.grid import Grid
from gui.button import Button


class MapWidget:
    """
      This class represent a map widget where maps
      are going to be placed.
    """
    
    def __init__(self, pos_x: float, pos_y: float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.width = 350
        self.height = 380
        self.btn_width = 90
        self.btn_height = 30

        self.main_rect = pygame.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.main_rect_color = (204, 230, 244)
        self.main_rect_border_radius = 12
        
        # Define button tab colors
        self.ally_map_selected = True
        self.selected_tab_color = '#72788D'
        self.unselected_tab_color = '#AEC301'
        
        # Define button tabs
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
        
        # Define ally and enemy maps
        self.ally_map = Grid(
          pos_x=self.pos_x + 15,
          pos_y=self.pos_y + 43
        )
        self.enemy_map = Grid(
          pos_x=self.pos_x + 15,
          pos_y=self.pos_y + 43
        )

    def draw(self, window: pygame.display) -> None:
        """
          This function draws tab widget and selected map
          depending on which tab is selected on window.
        """
        
        # Draw main rect
        pygame.draw.rect(window, self.main_rect_color, self.main_rect,
                         border_radius=self.main_rect_border_radius)
        
        # Draw button tabs
        self.ally_tab_btn.draw(window)
        self.enemy_tab_btn.draw(window)
        
        # Draw map of current tab
        if self.ally_map_selected:
            self.ally_map.draw(window)
        else:
            self.enemy_map.draw(window)  
    
    def handle_button_tabs_events(self) -> None:
        """
          This function handles button tab widget click events
          to keep tracking current selected tab.
        """
        
        if self.ally_tab_btn.click():
            self.ally_map_selected = True
            self.ally_tab_btn.change_top_colors(self.selected_tab_color)
            self.enemy_tab_btn.change_top_colors(self.unselected_tab_color)
        if self.enemy_tab_btn.click():
            self.ally_map_selected = False
            self.ally_tab_btn.change_top_colors(self.unselected_tab_color)
            self.enemy_tab_btn.change_top_colors(self.selected_tab_color)
