import pygame
from typing import Tuple, List
from gui.grid import Grid
from gui.button import Button


class Ship:
    """
      This class handles every ships common logic.
    """

    def __init__(self, image_path: str, pos_x: float, pos_y: float) -> None:
        self.image = pygame.image.load(image_path)
        self.life = None
        self.is_vertical = True  # Keep tracking of ship orientation
        self.name = 'Default'

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.inflate_value = (0, 0)
        self.collision_rect = self.rect

        self.can_rotate = True
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

    def is_inside_grid(self, grid: Grid) -> bool:
        """
          This method checks if ship is completely inside in grid.
          Collision have to be made with image rect in order to handle
          unexpected behaviour at grid boundaries.
        """
        return grid.rect.contains(self.rect)

    def is_colliding_with_ships(self, ships_collision_rect: List[pygame.Rect]) -> bool:
        """
          This method checks if ship is colliding with others ships.
          For this method, collision rect is used.
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
          This method moves ship by adding a delta to current
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
          This method calculates where to drop dragged ship in a valid 
          position of the grid.

          The main idea is to use ship.rect.center as a pivot in order to
          locate dragged ship.
        """
        
        position_without_offset = grid.center_position(self.rect.center)
        self.rect.center = position_without_offset
        self.collision_rect.center = position_without_offset

        self.rotate_btn.center_buttom_from_position(position_without_offset)

    def rotate_ship(self, grid: Grid, ships_collision_rect: List[pygame.Rect]) -> None:
        """
          This method rotates a ship and validates if 
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

    def draw(self, window: pygame.display) -> None:
        """
          This method draws ship on window.
        """
        window.blit(self.image, self.rect)
        self.draw_hitbox(window)
        self.draw_rect(window)

    def draw_hitbox(self, window: pygame.display) -> None:
        """
          This method draws ship collision rect and its center point on window.
        """

        color = (255, 0, 0)
        pygame.draw.rect(window, color, (self.collision_rect.x, self.collision_rect.y,
                                         self.collision_rect.width, self.collision_rect.height), 1, border_radius=1)
        pygame.draw.circle(window, color, self.collision_rect.center, 4)

    def draw_rect(self, window: pygame.display) -> None:
        """
          This method draws ship rect and its center point on window.
        """

        color = (13, 115, 13)
        pygame.draw.rect(window, color, (self.rect.x, self.rect.y,
                                         self.rect.width, self.rect.height), 1, border_radius=1)
        pygame.draw.circle(window, color, self.rect.center, 4)

    def __rotate_ship_image_and_rect(self, rollback: bool = False) -> None:
        """
          This private method rotates ship image and
          its rect.
        """

        degree = 90 if not rollback else -90
        current_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, degree)
        self.rect = self.image.get_rect(center=current_center)

    def __rotate_collision_rect(self) -> None:
        """
          This private method rotates ship collision rect.
          This method takes current ship rect and inflates
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
