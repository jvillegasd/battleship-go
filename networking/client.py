import json
import socket
import logging
from threading import Thread

from networking.decorator import thread_safe


BUFFER_SIZE = 4096

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.root.setLevel(logging.NOTSET)


class Client:
    """ This function represents client instance. """

    def __init__(self, client_name: str, host_address: str, host_port: int) -> None:
        self.client_name = client_name
        self.server_socket = None
        self.host_address = host_address
        self.host_port = host_port
        self.clients_tiles = {}

    def connect_to_server(self) -> None:
        """ This function creates a socket to connect to game server. """

        try:
            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.host_address, self.host_port))

            server_thread = Thread(target=self.server_listener,
                                   args=(self.server_socket, self.client_name))
            server_thread.start()
        except socket.error as error:
            logging.ERROR(error)

    def server_listener(self, server_socket: socket.socket, client_name: str) -> None:
        """ This function listen to server messages. """

        self.send_data_to_server(client_name)
        data = server_socket.recv(BUFFER_SIZE)
        ack = self.__decode_data(data)

        logging.info(f'Server ACK: {ack}')

        while True:
            data = server_socket.recv(BUFFER_SIZE)
            if not data:
                break

            decoded_data = self.__decode_data(data)
            logging.info(f'Received data: {decoded_data}')

            self.update_client_tiles(decoded_data)

        server_socket.close()

    def send_data_to_server(self, data: object) -> None:
        """ This function sends data to server. """

        message = json.dumps(data)
        self.server_socket.send(bytes(message, 'utf-8'))

    @thread_safe
    def update_client_tiles(self, new_clients_tiles: dict) -> None:
        """ This function updates client tiles. """
        self.clients_tiles = new_clients_tiles

    def __decode_data(self, data: bytes) -> object:
        """ This function decode data received from server. """
        return json.loads(data.decode('utf-8'))
