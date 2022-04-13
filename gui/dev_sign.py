import pygame

pygame.font.init()


class DevSign:
    """ This class represent the dev sign GUI element. """

    def __init__(self, pos_x: float, pos_y: float) -> None:
        # Define attributes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = 30
        self.height = 30
        self.sign = 'Made by jvillegasd :D'
        self.font = pygame.font.Font(
            'assets/fonts/CascadiaCode-SemiBold.ttf', 14)

        # Define colors
        self.text_color = '#72788D'

        # Define text rect
        self.sign_surf = self.font.render(self.sign, True, self.text_color)
        self.sign_rect = self.sign_surf.get_rect(
            topleft=(self.pos_x, self.pos_y))

    def draw(self, window: pygame.display) -> None:
        """ This function draws sign on window. """
        window.blit(self.sign_surf, self.sign_rect)
