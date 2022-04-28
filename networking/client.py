import socket
import logging
from typing import Union, List, Tuple

from networking.network import Network
from networking.constants import BUFFER_SIZE


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.root.setLevel(logging.NOTSET)


class Client(Network):
    """ This function represents client instance. """

    def __init__(self, client_name: str, host_address: str, host_port: int) -> None:
        self.is_disconnected = False
        self.client_name = client_name

        self.server_socket = None
        self.host_port = host_port
        self.host_address = host_address

    def connect_to_server(self) -> bool:
        """ This function creates a socket to connect to game server. """

        try:
            self.host_port = int(self.host_port)

            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.host_address, self.host_port))

            ack = self.send_data_to_server(self.client_name)
            logging.info(f'Server ACK: {ack}')

            return True
        except TypeError as error:
            logging.error(error)
        except ValueError as error:
            logging.error(error)
        except socket.error as error:
            logging.error(error)

        return False

    def disconnect(self) -> None:
        """ This function send a disconnected request to server. """

        self.is_disconnected = True
        self.send_data_to_server({'request': 'disconnect'})
        logging.info('Client disconnected')

    def send_data_to_server(self, data: object) -> Union[dict, None]:
        """ This function sends data and receive response from server. """

        try:
            message = self.create_datagram(BUFFER_SIZE, data)
            self.server_socket.sendall(message)

            response = self.server_socket.recv(BUFFER_SIZE)
            if response:
                return self.decode_data(response)
        except socket.error:
            logging.info('Client disconnected by server')
            self.is_disconnected = True

        return None

    def lock_ships(self, game_grid: List[list]) -> None:
        """ Notify to server that client locked ships and send game grid """
        self.send_data_to_server({'request': 'ship_locked', 'grid': game_grid})

    def attack_enemy_tile(self, position: Tuple[float, float]) -> str:
        """ Request an attack to enemy grid. """
        
        response = self.send_data_to_server({'request': 'attack_tile', 'position': position})
        return response.get('attacked')

    def is_my_turn(self) -> bool:
        """ This function checks if it is client turn. """

        game_data = self.get_game_data()
        return game_data[self.client_name]['my_turn']

    def ship_sinked(self) -> None:
        """ Notify that a ship is sinked. """
        self.send_data_to_server({'request': 'ship_sinked'})

    def get_game_data(self) -> Union[dict, None]:
        """ Request current game data to server. """

        response = self.send_data_to_server({'request': 'game_data'})
        return response

    def get_game_status(self) -> Union[dict, None]:
        """ Request to server if game started. """

        response = self.send_data_to_server({'request': 'game_status'})
        return response.get('game_status')

    def get_winner(self) -> Union[dict, None]:
        """ Request to server winner username. """

        response = self.send_data_to_server({'request': 'winner'})
        return response.get('winner')

    def reset_game(self) -> None:
        """ Request to reset game. """
        self.send_data_to_server({'request': 'reset_game'})
