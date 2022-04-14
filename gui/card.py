import pygame


class Card:
    """ This class represents a card GUI element. """

    def __init__(
            self,
            pos_x: float,
            pos_y: float,
            width: float,
            height: float,
            card_color: str = '#E6F0CC',
            border_radius: int = 12) -> None:
        # Define attributes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.card_color = card_color
        self.shadow_color = '#BEBEBE'
        self.shadow_offset = (5, 5)
        self.border_radius = border_radius

        # Define main rect
        self.main_rect = pygame.Rect(
            (self.pos_x, self.pos_y), (self.width, self.height))

        # Define shadows
        self.shadow_rect = pygame.Rect(
            (self.pos_x + self.shadow_offset[0],
             self.pos_y + self.shadow_offset[1]),
            (self.width, self.height))

    def draw(self, window: pygame.display) -> None:
        """ This method draws card on window. """

        # Draw shadow rect
        pygame.draw.rect(window, self.shadow_color,
                         self.shadow_rect, border_radius=self.border_radius)

        # Draw main rect
        pygame.draw.rect(window, self.card_color, self.main_rect,
                         border_radius=self.border_radius)
