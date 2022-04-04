import pygame
from typing import Tuple, List

from stages.intro import Intro

WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')

# Color name: Little Greene French Grey Pale
BACKGROUND_COLOR = (231, 231, 219)

FPS = 30


class GameState:

    def __init__(self) -> None:
        self.state = 'intro'
        self.intro_stage = Intro()
    
    def intro(self) -> None:
        states = self.intro_stage.process_events()
        self.intro_stage.draw(WIN)
        
    
    def state_manager(self) -> None:
      if self.state == 'intro':
          self.intro()
      
      
      


game_state = GameState()


def main():
  while True:
    game_state.state_manager()


if __name__ == '__main__':
    main()
