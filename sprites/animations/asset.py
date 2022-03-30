import os
import pygame
from typing import Tuple


class AssetAnimation:
    """
      This class handle common logic of asset animation.
    """

    def __init__(self, animation_path: str, pos_x: float, pos_y: float) -> None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.index = 0
        self.images = []
        for image_file in os.listdir(animation_path):
            image_path = os.path.join(animation_path, image_file)
            self.images.append(pygame.image.load(image_path))

        # Animation rect
        self.rect = self.images[0].get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
        # Animation speed reduction
        self.slow_animation_factor = 2
        self.slow_animation_cnt = 0

    def draw(self, window: pygame.display) -> None:
        """
          This function draws current frame of
          animation on window.
        """
        
        image = self.__calculate_current_frame()
        window.blit(image, self.rect)
    
    def animation_finished(self) -> bool:
        return self.index >= len(self.images)

    def center_animation_from_position(self, position: Tuple[float, float]) -> None:
        self.rect.center = position

    def __calculate_current_frame(self) -> pygame.image:
        """
          This function calculates current frame of
          animation. In order to keep animation
          smooth, it was slowered by a specific factor.
        """
        
        if self.animation_finished():
            self.index = 0
        image = self.images[self.index]
        
        # Make animation slower than FPS
        self.slow_animation_cnt += 1
        if self.slow_animation_cnt > self.slow_animation_factor:
            self.index += 1
            self.slow_animation_cnt = 0

        return image
