import os
import pygame

pygame.font.init()
GUI_FONT = pygame.font.Font(None, 30)


class Button:
    # https://www.youtube.com/watch?v=8SzTzvrWaAA&list=PLIqh2QXT_ndYs0GpAQ2Eldup4eLUoCDC-&index=12
    def __init__(self,
                 text: str,
                 pos_x: float,
                 pos_y: float,
                 width: float,
                 height: float,
                 btn_color: str = '#4C6785',
                 text_color: str = '#4FA4B8') -> None:
        super().__init__()

        self.pressed = False

        self.top_rect = pygame.Rect(pos_x, pos_y, width, height)
        self.top_color = btn_color

        self.text_surf = GUI_FONT.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, window: pygame.display) -> None:
        """
          This method draws button on window. 
        """

        pygame.draw.rect(window, self.top_color,
                         self.top_rect, border_radius=12)
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
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                action = True
                self.pressed = True
            elif not pygame.mouse.get_pressed()[0]:
                self.pressed = False

        return action
