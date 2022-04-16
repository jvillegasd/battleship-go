import json
import socket
import logging
from threading import Thread

from networking.network import Network
from networking.decorator import thread_safe
from networking.constants import BUFFER_SIZE


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.root.setLevel(logging.NOTSET)


class Client(Network):
    """ This function represents client instance. """

    def __init__(self, client_name: str, host_address: str, host_port: int) -> None:
        self.is_game_started = False
        self.is_disconnected = False
        self.client_name = client_name
        
        self.clients_tiles = {}
        
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

    def send_data_to_server(self, data: object) -> dict:
        """ This function sends data and receive response from server. """

        message = self.create_datagram(BUFFER_SIZE, data)
        self.server_socket.sendall(message)
        
        response = self.server_socket.recv(BUFFER_SIZE)
        return self.decode_data(response)
    
    def get_game_data(self) -> dict:
        """ Request current game data to server. """
        
        response = self.send_data_to_server({'request': 'game_data'})
        return response

    def get_game_status(self) -> str:
        """ Request to server if game started. """
        
        response = self.send_data_to_server({'request': 'game_status'})
        return response['game_status']

    def get_winner(self) -> str:
        """ Request to server winner username. """

        response = self.send_data_to_server({'request': 'winner'})
        return response['winner']
