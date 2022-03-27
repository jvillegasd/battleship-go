import pygame
from typing import Tuple

pygame.font.init()
GUI_FONT = pygame.font.Font('assets/fonts/CascadiaCode-SemiBold.ttf', 14)


class Button:
    """
      This class represent a button GUI element for PyGame.
      Resource: https://youtu.be/8SzTzvrWaAA
    """

    def __init__(self,
                 text: str,
                 pos_x: float,
                 pos_y: float,
                 width: float,
                 height: float,
                 elevation: int = 6,
                 border_radius: int = 12,
                 btn_color: str = '#475F77',
                 btn_bottom_color: str = '#354B5E',
                 btn_hover_color: str = '#D74B4B',
                 text_color: str = '#FFFFFF') -> None:
        super().__init__()

        # Core attributes
        self.pressed = False

        # Button colors
        self.top_color = btn_color
        self.current_top_color = btn_color
        self.top_hover_color = btn_hover_color
        self.bottom_color = btn_bottom_color

        # Elevation and radius
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_pos_y = pos_y
        self.border_radius = border_radius

        # Top rectangle
        self.top_rect = pygame.Rect(pos_x, pos_y, width, height)

        # Text rectangle
        self.text_surf = GUI_FONT.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(pos_x, pos_y, width, self.elevation)
    
    def center_buttom_from_position(self, position: Tuple[float, float]) -> None:
          """
            This method centers the buttom over provided position.
          """
          
          self.top_rect.center = position
          self.bottom_rect.center = position
          self.text_rect.center = position
          
          self.original_pos_y = position[1]

    def draw(self, window: pygame.display) -> None:
        """
          This method draws button on window. 
        """

        # Elevation logic
        self.top_rect.y = self.original_pos_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        # Draw bottom button
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(window, self.bottom_color,
                         self.bottom_rect, border_radius=self.border_radius)

        # Draw top button
        pygame.draw.rect(window, self.current_top_color,
                         self.top_rect, border_radius=self.border_radius)
        window.blit(self.text_surf, self.text_rect)

    def click(self) -> None:
        """
          This method checks if button was clicked. Verify if
          button is still pressed in order to do not execute button
          action everytime until mouse click is released.
        """

        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.dynamic_elevation = 0
            self.current_top_color = self.top_hover_color
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                action = True
                self.pressed = True
            elif not pygame.mouse.get_pressed()[0]:
                self.pressed = False
                self.dynamic_elevation = self.elevation
        else:
            self.dynamic_elevation = self.elevation
            self.current_top_color = self.top_color

        return action
