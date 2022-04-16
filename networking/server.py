import socket
import logging
from typing import List
from threading import Thread

from networking.network import Network
from networking.decorator import thread_safe
from networking.constants import CONN_LIMIT, BUFFER_SIZE


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.root.setLevel(logging.NOTSET)


class Server(Network):
    """ This class represents server instance. """

    def __init__(self, host_address: str, host_port: int) -> None:
        self.server_socket = None
        self.host_address = host_address
        self.host_port = host_port
        self.game_data = {
            'clients': {},
            'sockets': {}
        }

    def start_server(self) -> None:
        """ This function creates a server socket and start a thread for listening. """

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_address, self.host_port))
        self.server_socket.listen(CONN_LIMIT)

        server_thread = Thread(target=self.server_lobby)
        server_thread.start()

    def stop_server(self) -> None:
        """ This function stops current server. """

        for client_name in self.game_data['sockets']:
            self.game_data['sockets'][client_name].shutdown(socket.SHUT_RDWR)
            self.game_data['sockets'][client_name].close()

        self.server_socket.close()

    def server_lobby(self) -> None:
        """ This function handles server lobby, waiting for every player is connected. """

        logging.info('Server started!')
        try:
            while True:
                if len(self.game_data['clients']) < CONN_LIMIT:
                    client, address = self.server_socket.accept()

                    client_thread = Thread(
                        target=self.client_listener, args=(client, address))
                    client_thread.start()
        except socket.error:
            logging.info('Server stopped.')

    def client_listener(self, client_socket: socket.socket, client_ip: str):
        """ This function listens to clients messages and processes them. """

        socket_disconnected = False

        data = client_socket.recv(BUFFER_SIZE)
        client_name = self.decode_data(data)

        self.__add_client_to_server(client_name, client_socket)
        self.send_data_to_client('Connected', client_name)

        logging.info(f'Client connected: {client_name}')

        # Notify to other clients that a new player is connected
        if len(self.game_data['clients']) > 1:
            self.send_data_to_clients(self.game_data['clients'], client_name)
        
        if len(self.game_data['clients']) == CONN_LIMIT:
            self.send_data_to_clients({'message': 'Game started'})

        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                decoded_data = self.decode_data(data)
                logging.info(f'Received_data: {decoded_data}')

                if 'reset_game' in decoded_data:
                    self.reset_game_data()
                elif 'disconnect' in decoded_data:
                    logging.info(f'Client disconnected: {client_name}')
                    break
                elif 'game_data' in decoded_data:
                    self.update_game_data(decoded_data['data'])

                self.send_data_to_clients(
                    self.game_data['clients'], client_name)
        except socket.error:
            socket_disconnected = True
            logging.info(f'Client socket disconnected: {client_name}')

        self.__remove_client_from_server(client_name)
        if not socket_disconnected:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

    @thread_safe
    def send_data_to_clients(self, data: object, sender_name: str = None) -> None:
        """ This function sends data to all clients. """

        message = self.create_datagram(BUFFER_SIZE, data)
        for client_name in self.game_data['sockets']:
            if client_name != sender_name:
                self.game_data['sockets'][client_name].sendall(message)

    @thread_safe
    def send_data_to_client(self, data: object, client_name: str) -> None:
        """ This function sends data to a specific client. """

        message = self.create_datagram(BUFFER_SIZE, data)
        self.game_data['sockets'][client_name].sendall(message)

    @thread_safe
    def update_game_data(self, new_game_data: dict) -> None:
        """ This function updates game data. """
        self.game_data['clients'] = new_game_data

    @thread_safe
    def reset_game_data(self) -> None:
        """ This function reset game data. """

        for client_name in self.game_data['clients']:
            self.game_data['clients'][client_name]['attacked_tile'] = None

    @thread_safe
    def get_connected_clients(self) -> List[str]:
        """ This function returns connected clients. """
        return self.game_data['clients'].keys()

    @thread_safe
    def __add_client_to_server(
            self,
            client_name: str,
            client_socket: socket.socket) -> None:
        """ This function adds a client to game_data. """

        self.game_data['clients'][client_name] = {
            'attacked_tile': None,
            'ship_locked': False,
            'my_turn': False
        }
        self.game_data['sockets'][client_name] = client_socket

    @thread_safe
    def __remove_client_from_server(self, client_name: str) -> None:
        """ This function removes client from game_data. """
        self.game_data['clients'].pop(client_name, None)
        self.game_data['sockets'].pop(client_name, None)