import pygame

pygame.font.init()
GUI_FONT = pygame.font.Font('assets/fonts/CascadiaCode-SemiBold.ttf', 14)


class Input:
    """ This class represents a text input GUI element. """

    def __init__(
            self,
            pos_x: float,
            pos_y: float,
            width: float,
            height: float,
            border_radius: int = 10,
            text_color: str = '#475F77',
            input_color: str = '#CCE6EC',
            shadow_color: str = '#475F77') -> None:
        # Define attributes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        
        # Input tracking variable
        self.input_text: str = 'a'

        # Define gui properties
        self.text_color = text_color
        self.input_color = input_color
        self.shadow_color = shadow_color
        self.border_radius = border_radius

        # Define text rect
        self.input_surf = GUI_FONT.render(
            self.input_text, True, self.text_color)
        self.input_rect = self.input_surf.get_rect(
            topleft=(self.pos_x, self.pos_y), width=self.width, height=self.height)

        # Define text rect shadow
        self.input_shadow_rect = self.input_rect.inflate(6, 6)

    def draw(self, window: pygame.display) -> None:
        # Draw shadows
        pygame.draw.rect(window, self.shadow_color,
                         self.input_shadow_rect, border_radius=self.border_radius)

        # Draw input rect
        pygame.draw.rect(window, self.input_color,
                         self.input_rect, border_radius=self.border_radius)

        # Draw text
        window.blit(self.input_surf, self.input_rect)
