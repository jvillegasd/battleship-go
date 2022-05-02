import pygame
from typing import Tuple, List

from gui.grid import Grid
from gui.button import Button
from gui.text_bubble import TextBubble


class Ship:
    """
      This class handles every ships common logic.
    """
    
    def __init__(self, image_path: str, pos_x: float, pos_y: float) -> None:
        # Define core attributes
        self.image = pygame.image.load(image_path)
        self.is_vertical = True  # Keep tracking of ship orientation
        self.name = 'Default'

        # Define ship life
        self.life = 1
        self.current_life = 1

        # Define ship rect
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        # Define collision rect
        self.inflate_value = (0, 0)
        self.collision_rect = self.rect

        # Define rotate button
        self.can_rotate = True
        self.can_draw_button = False
        self.rotate_btn = Button(
            text=">",
            pos_x=self.rect.center[0],
            pos_y=self.rect.center[1],
            width=20,
            height=20,
            btn_color='#AEC301',
            btn_bottom_color='#64734c',
            btn_hover_color='#637001'
        )
        self.rotate_btn.center_buttom_from_position(self.rect.center)

        # Define text bubble
        self.can_draw_bubble = False
        self.life_diplay = TextBubble(
            pos_x=self.rect.center[0],
            pos_y=self.rect.center[1],
            width=80,
            height=20,
            text=f'Life: {self.current_life}/{self.life}'
        )
        self.life_diplay.center_button_from_position(self.rect.center)

    def is_inside_grid(self, grid: Grid) -> bool:
        """
          This function checks if ship is completely inside in grid.
          Collision have to be made with image rect in order to handle
          unexpected behaviour at grid boundaries.
        """
        return grid.rect.contains(self.rect)

    def is_colliding_with_ships(self, ships_collision_rect: List[pygame.Rect]) -> bool:
        """
          This function checks if ship is colliding with others ships.
          For this function, collision rect is used.
        """

        collided_ships = self.collision_rect.collidelistall(
            ships_collision_rect)
        return len(collided_ships) > 1

    def move_ship(
            self,
            delta: Tuple[float, float],
            grid: Grid,
            ships_collision_rect: List[pygame.Rect]) -> None:
        """
          This function moves ship by adding a delta to current
          rect position. If final position lets ship outside
          the grid, the ship is moved to inital position.
        """

        self.rect.x += delta[0]
        self.rect.y += delta[1]

        self.collision_rect.x += delta[0]
        self.collision_rect.y += delta[1]

        if not self.is_inside_grid(grid) or self.is_colliding_with_ships(ships_collision_rect):
            self.rect.x -= delta[0]
            self.rect.y -= delta[1]

            self.collision_rect.x -= delta[0]
            self.collision_rect.y -= delta[1]

    def dragged_ship_position(self, grid: Grid) -> None:
        """
          This function calculates where to drop dragged ship in a valid 
          position of the grid.

          The main idea is to use ship.rect.center as a pivot in order to
          locate dragged ship.
        """

        position_without_offset = grid.center_position(self.rect.center)
        self.rect.center = position_without_offset
        self.collision_rect.center = position_without_offset

        self.rotate_btn.center_buttom_from_position(position_without_offset)
        self.life_diplay.center_button_from_position(position_without_offset)

    def rotate_ship(self, grid: Grid, ships_collision_rect: List[pygame.Rect]) -> None:
        """
          This function rotates a ship and validates if 
          final position lets it inside the provided grid.
        """

        # Change ship orientation
        self.is_vertical = not self.is_vertical

        # Rotate image and its rect
        self.__rotate_ship_image_and_rect()

        # Rotate collision rect
        self.__rotate_collision_rect()

        if not self.is_inside_grid(grid) or self.is_colliding_with_ships(ships_collision_rect):
            # Rollback ship orientation
            self.is_vertical = not self.is_vertical

            # Rollback image and its rect rotation
            self.__rotate_ship_image_and_rect(rollback=True)

            # Rollback collision rect rotation
            self.__rotate_collision_rect()

    def set_ship_life(self, life: int) -> None:
        """ This function assign life to current ship. """

        self.life = life
        self.current_life = life
        self.life_diplay.change_text(f'life: {self.current_life}/{self.life}')

    def get_ship_life(self) -> int:
        """ This function returns current ship life. """
        return self.current_life

    def get_attacked(self) -> int:
        """
          This function substracts 1 point of live
          everytime the ships get attacked. 
        """

        if self.current_life > 0:
            self.current_life -= 1
            self.life_diplay.change_text(
                f'life: {self.current_life}/{self.life}')

        return self.current_life

    def draw(self, window: pygame.display) -> None:
        """
          This function draws ship, rotate button
          and text bubble on window.
        """
        
        window.blit(self.image, self.rect)
        
        if self.can_draw_button:
            self.rotate_btn.draw(window)
        
        if self.can_draw_bubble:
            self.life_diplay.draw(window)

    def draw_hitbox(self, window: pygame.display) -> None:
        """
          This function draws ship collision rect and its center point on window.
        """

        color = (255, 0, 0)
        pygame.draw.rect(window, color, (self.collision_rect.x, self.collision_rect.y,
                                         self.collision_rect.width, self.collision_rect.height), 1, border_radius=1)
        pygame.draw.circle(window, color, self.collision_rect.center, 4)

    def draw_rect(self, window: pygame.display) -> None:
        """
          This function draws ship rect and its center point on window.
        """

        color = (13, 115, 13)
        pygame.draw.rect(window, color, (self.rect.x, self.rect.y,
                                         self.rect.width, self.rect.height), 1, border_radius=1)
        pygame.draw.circle(window, color, self.rect.center, 4)

    def rotate_button_click(self) -> bool:
        return self.can_draw_button and self.rotate_btn.click()

    def __rotate_ship_image_and_rect(self, rollback: bool = False) -> None:
        """
          This private function rotates ship image and
          its rect.
        """

        degree = 90 if not rollback else -90
        current_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, degree)
        self.rect = self.image.get_rect(center=current_center)

    def __rotate_collision_rect(self) -> None:
        """
          This private function rotates ship collision rect.
          This function takes current ship rect and inflates
          depeding on tracked orientation.
        """

        self.collision_rect = self.rect

        # Inflate collision rect depending on orientation
        if not self.is_vertical:
            self.collision_rect = self.rect.inflate((
                self.inflate_value[1],
                self.inflate_value[0]
            ))
        else:
            self.collision_rect = self.rect.inflate((
                self.inflate_value[0],
                self.inflate_value[1]
            ))
