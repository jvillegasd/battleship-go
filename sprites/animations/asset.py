import os
import pygame


class AssetAnimation:
    """
      This class handle common logic of asset animation.
    """

    def __init__(self, animation_path: str, pos_x: float, pos_y: float) -> None:
        self.index = 0
        self.images = []
        for image_file in os.listdir(animation_path):
            image_path = os.path.join(animation_path, image_file)
            self.images.append(pygame.image.load(image_path))

        self.rect = self.images[0].get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, window: pygame.display):
        """
          This method draws current frame of
          animation on window.
        """
        
        image = self.__calculate_current_frame()
        window.blit(image, self.rect)

    def __calculate_current_frame(self) -> pygame.image:
        """
          This method calculates current frame of
          animation.
        """
        
        if self.index >= len(self.images):
            self.index = 0
        image = self.images[self.index]
        self.index += 1

        return image
