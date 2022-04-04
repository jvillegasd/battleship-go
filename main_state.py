import pygame
from typing import Tuple, List

from stages.intro import Intro
from stages.ship_location import ShipLocation

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
        self.ship_location_stage = ShipLocation()
    
    def intro(self) -> None:
        states = self.intro_stage.process_events()
        self.intro_stage.draw(WIN)
        
        if states['game_started']:
            self.state = 'ship_location'

    def ship_location(self) -> None:
        states = self.ship_location_stage.process_events()
        self.ship_location_stage.draw(WIN)
    
    def state_manager(self) -> None:
      if self.state == 'intro':
          self.intro()
      elif self.state == 'ship_location':
          self.ship_location()
      
      


game_state = GameState()


def main():
  while True:
    game_state.state_manager()


if __name__ == '__main__':
    main()
