import enum
import socket
import logging
from typing import List, Tuple
from threading import Thread

from networking.network import Network
from networking.decorator import thread_safe
from networking.constants import CONN_LIMIT, BUFFER_SIZE, SHIPS_NAMES


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.root.setLevel(logging.NOTSET)


class GameStatus(enum.Enum):
    lobby = 1
    ship_lock = 2
    battle = 3
    finished = 4
    player_disconnected = 5


class Server(Network):
    """ This class represents server instance. """

    def __init__(self, host_address: str, host_port: int) -> None:
        self.is_first_player = True
        self.server_socket = None
        self.host_address = host_address
        self.host_port = host_port
        self.game_data = {
            'winner': None,
            'game_status': GameStatus['lobby'].name,
            'game_grid': {},
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

        self.end_game()
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

        logging.info(
            f'Client "{client_name}" connected from IP: "{client_ip}"')

        if len(self.game_data['clients']) == CONN_LIMIT:
            self.game_data['game_status'] = GameStatus['ship_lock'].name

        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break

                decoded_data = self.decode_data(data)
                logging.info(f'Received data: {decoded_data}')

                if (
                    self.game_data['game_status'] == GameStatus['ship_lock'].name
                    and self.check_if_ships_are_locked()
                ):
                    self.game_data['game_status'] = GameStatus['battle'].name

                if (
                    self.game_data['game_status'] == GameStatus['battle'].name
                    and self.game_data['winner']
                ):
                    self.game_data['game_status'] = GameStatus['finished'].name

                if 'request' in decoded_data:
                    if decoded_data['request'] == 'ship_locked':
                        self.game_data['clients'][client_name]['ship_locked'] = True
                        self.game_data['game_grid'][client_name] = decoded_data['grid']
                        
                        self.send_data_to_client(
                            {'message': 'ok'}, client_name)

                    if decoded_data['request'] == 'reset_game':
                        self.reset_game()
                        self.send_data_to_client(
                            {'message': 'ok'}, client_name)

                    if decoded_data['request'] == 'disconnect':
                        logging.info(f'Client disconnected: {client_name}')
                        break

                    if decoded_data['request'] == 'game_data':
                        self.send_data_to_client(
                            self.game_data['clients'], client_name)

                    if decoded_data['request'] == 'game_status':
                        self.send_data_to_client(
                            {'game_status': self.game_data['game_status']}, client_name)

                    if decoded_data['request'] == 'winner':
                        self.send_data_to_client(
                            {'winner': self.game_data['winner']}, client_name)

                    if decoded_data['request'] == 'attack_tile':
                        ship_name = self.attack_enemy_tile(
                            client_name, decoded_data['position'])
                        self.game_data['clients'][client_name]['attacked_tile'] = {
                            'position': decoded_data['position'],
                            'ship_name': ship_name
                        }
                        
                        self.send_data_to_client(
                            {'attacked': ship_name}, client_name)

                    if decoded_data['request'] == 'ship_sinked':
                        self.game_data['clients'][client_name]['sinked_ships'] += 1
                        if self.game_data['clients'][client_name]['sinked_ships'] >= len(SHIPS_NAMES):
                            self.game_over(client_name)
                        
                        self.send_data_to_client(
                            {'message': 'ok'}, client_name)
                else:
                    self.send_data_to_client({'message': 'ok'}, client_name)
        except socket.error:
            socket_disconnected = True
            logging.info(f'Client disconnected by server: {client_name}')

        self.__remove_client_from_server(client_name)
        if not socket_disconnected:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

            logging.info(f'Closing game')
            self.end_game()

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
    def end_game(self) -> None:
        """ This function ends game by cleaning server connections. """

        for client_name in self.game_data['sockets']:
            self.game_data['sockets'][client_name].shutdown(socket.SHUT_RDWR)
            self.game_data['sockets'][client_name].close()

        self.is_first_player = True
        self.game_data['clients'] = {}
        self.game_data['winner'] = None
        self.game_data['game_status'] = GameStatus['player_disconnected'].name

    @thread_safe
    def reset_game(self) -> None:
        """ This function reset game data. """

        self.is_first_player = True
        for client_name in self.game_data['clients']:
            self.game_data['clients'][client_name] = {
                'attacked_tile': {
                    'ship_name': None,
                    'position': None
                },
                'sinked_ships': 0,
                'ship_locked': False,
                'my_turn': self.is_first_player
            }
            self.is_first_player = False
            self.game_data['game_grid'][client_name] = None

        self.game_data['winner'] = None
        self.game_data['game_status'] = GameStatus['ship_lock'].name

    @thread_safe
    def check_if_ships_are_locked(self) -> bool:
        """ This function checks clients locked their ships. """
        return all(
            self.game_data['game_grid'][client_name] is not None
            for client_name in self.game_data['game_grid'])

    @thread_safe
    def game_over(self, loser_name: str) -> None:
        """
          This function looks for the winner name by filtering using loser name.

          Server maintain a tracking of players grids an their attacks attemps,
          but clients notifies when a ship sinks.
        """
        self.game_data['winner'] = next(
            (
                client_name
                for client_name in self.game_data['clients']
                if client_name != loser_name
            ), None)

    @thread_safe
    def attack_enemy_tile(self, attacker_name: str, position: Tuple[float, float]) -> str:
        """ This function checks if position hits an enemy ship and updates turn. """

        # Update players turn and get enemy grid
        enemy_grid = None
        for client_name in self.game_data['clients']:
            if client_name == attacker_name:
                self.game_data['clients'][client_name]['my_turn'] = False
            else:
                enemy_grid = self.game_data['game_grid'][client_name]
                self.game_data['clients'][client_name]['my_turn'] = True

        if (
            enemy_grid
            and enemy_grid[position[1]][position[0]] in SHIPS_NAMES
        ):
            ship_name = enemy_grid[position[1]][position[0]]
            enemy_grid[position[1]][position[0]] = 'X'
            return ship_name

        return None

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
            'attacked_tile': {
                'ship_name': None,
                'position': None
            },
            'sinked_ships': 0,
            'ship_locked': False,
            'my_turn': self.is_first_player
        }
        self.game_data['game_grid'][client_name] = None
        self.game_data['sockets'][client_name] = client_socket
        self.is_first_player = False

    @thread_safe
    def __remove_client_from_server(self, client_name: str) -> None:
        """ This function removes client from game_data. """
        self.game_data['clients'].pop(client_name, None)
        self.game_data['sockets'].pop(client_name, None)
        self.game_data['game_grid'].pop(client_name, None)
