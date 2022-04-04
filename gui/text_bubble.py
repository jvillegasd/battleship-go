import pygame

pygame.font.init()
GUI_FONT = pygame.font.Font('assets/fonts/CascadiaCode-SemiBold.ttf', 14)


class TextBubble:
    """ This class represent a text bubble GUI element for PyGame. """

    def __init__(
            self,
            pos_x: float,
            pos_y: float,
            width: float,
            height: float,
            text: str,
            bubble_color: str = '#AEC301',
            shadow_color: str = '#72788D',
            text_color: str = '#FFFFFF') -> None:
        # Define attributes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

        # Define colors
        self.bubble_color = bubble_color
        self.shadow_color = shadow_color
        self.text_color = text_color

        # Define bubble rect
        self.bubble_rect = pygame.Rect(
            (self.pos_x, self.pos_y), (self.width, self.height))
        
        # Define bubble shadow rect
        self.bubble_shadow_rect = self.bubble_rect.inflate(6, 6)

        # Define bubble triangle
        triangle_pivot = pygame.Vector2(self.bubble_rect.bottomleft) + (16, 0)
        self.triangle_points = [
            triangle_pivot,
            triangle_pivot + (15, 0),
            triangle_pivot + (0, 15)
        ]
        
        # Define bubble triangle shadow
        triangle_shadow_pivot = pygame.Vector2(
            self.bubble_rect.bottomleft) + (13, 0)
        self.triangle_shadow_points = [
            triangle_shadow_pivot,
            triangle_shadow_pivot + (23, 0),
            triangle_shadow_pivot + (0, 23)
        ]
        
        # Define text rect
        self.text_surf = GUI_FONT.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.bubble_rect.center)

    def draw(self, window: pygame.display) -> None:
        # Draw shadows
        pygame.draw.rect(window, self.shadow_color,
                         self.bubble_shadow_rect, border_radius=12)
        pygame.draw.polygon(window, self.shadow_color,
                            self.triangle_shadow_points)
        
        # Draw bubble and triangle
        pygame.draw.rect(window, self.bubble_color,
                         self.bubble_rect, border_radius=12)
        pygame.draw.polygon(window, self.bubble_color, self.triangle_points)
        
        # Draw text
        window.blit(self.text_surf, self.text_rect)

    def change_text(self, new_text: str) -> None:
        self.text_surf = GUI_FONT.render(new_text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.bubble_rect.center)
