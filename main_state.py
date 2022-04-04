import pygame

# Import stages
from stages.intro import Intro
from stages.battle import Battle
from stages.ship_location import ShipLocation


FPS = 30
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battleship')


class GameState:
    """
      This class manages game states in a way to modularize
      stages and keep codebase organized.
      Resource: https://www.youtube.com/watch?v=j9yMFG3D7fg
    """

    def __init__(self) -> None:
        self.state = 'intro'
        self.intro_stage = Intro()
        self.ship_location_stage = ShipLocation()
        self.battle_stage = Battle()

    def intro(self) -> None:
        """ Intro stage state handler. """
        
        states = self.intro_stage.process_events()
        self.intro_stage.draw(WIN)

        if states['game_started']:
            self.state = 'ship_location'

    def ship_location(self) -> None:
        """ Ship location stage state handler. """

        states = self.ship_location_stage.process_events()
        self.ship_location_stage.draw(WIN)

        if states['ship_locked']:
            self.state = 'battle'
            map_widget, ships = self.ship_location_stage.get_maps_and_ships()
            self.battle_stage.load_maps_and_ships(map_widget, ships)

    def battle(self) -> None:
        """ Battle stage state handler. """
        
        states = self.battle_stage.process_events()
        self.battle_stage.draw(WIN)

    def state_manager(self) -> None:
        """ This function keeps tracking of current game state. """
      
        if self.state == 'intro':
            self.intro()
        elif self.state == 'ship_location':
            self.ship_location()
        elif self.state == 'battle':
            self.battle()


def main():
    game_state = GameState()
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)  # Force game loop to run at FPS limit
        game_state.state_manager()


if __name__ == '__main__':
    main()
