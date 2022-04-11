import json
import socket
import logging
from threading import Thread

from networking.network import Network
from networking.decorator import thread_safe
from networking.constans import CONN_LIMIT, BUFFER_SIZE


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

        closed_by_server = False
        
        data = client_socket.recv(BUFFER_SIZE)
        client_name = self.decode_data(data)

        self.game_data['clients'][client_name] = {'attacked_tile': None}
        self.game_data['sockets'][client_name] = client_socket
        self.send_data_to_client('Connected', client_name)

        logging.info(f'Client connected: {client_name}')

        if len(self.game_data['clients']) > 1:
            self.send_data_to_clients(self.game_data['clients'], client_name)

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
                else:
                    self.update_game_data(decoded_data)

                self.send_data_to_clients(
                    self.game_data['clients'], client_name)
        except socket.error:
            closed_by_server = True
            logging.info(f'Client disconnected by server: {client_name}')

        self.game_data['clients'].pop(client_name, None)
        self.game_data['sockets'].pop(client_name, None)

        if not closed_by_server:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

    @thread_safe
    def send_data_to_clients(self, data: object, sender_name: str) -> None:
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
