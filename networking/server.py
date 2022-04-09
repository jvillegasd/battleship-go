from email.header import decode_header
import json
import socket
from threading import Thread

# TODO: Change print to Logging

CONN_LIMIT = 2
BUFFER_SIZE = 4096
HEADER_SIZE = 10

game_data = {
    'clients': {},
    'sockets': {}
}

server_socket = None
host_address = 'localhost'
host_port = 65432


def start_server():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_address, host_port))
    server_socket.listen(CONN_LIMIT)

    server_thread = Thread(target=server_lobby, args=(server_socket, ''))
    server_thread.start()


def server_lobby(server_socket: socket.socket, client_address: str):
    global game_data

    while True:
        if len(game_data['clients']) < CONN_LIMIT:
            client, address = server_socket.accept()

            client_thread = Thread(
                target=client_listener, args=(client, address))
            client_thread.start()


def send_data_to_clients(data: object, sender_name: str):
    global game_data

    message = json.dumps(data)
    for client_name in game_data['sockets']:
        if client_name != sender_name:
            game_data['sockets'][client_name].send(bytes(message, 'utf-8'))


def send_data_to_client(data: object, client_name: str):
    global game_data

    message = json.dumps(data)
    game_data['sockets'][client_name].send(bytes(message, 'utf-8'))


def client_listener(client_socket: socket.socket, client_ip: str):
    global server_socket, game_data

    client_name = client_socket.recv(BUFFER_SIZE)
    game_data['clients'][client_name] = {'attacked_tile': None}
    game_data['sockets'][client_name] = client_socket
    send_data_to_client('Connected', client_name)

    if len(game_data['clients']) > 1:
        send_data_to_clients(game_data['clients'], client_name)

    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break

        decoded_data = json.loads(data.decode('utf-8'))
        if decoded_data == 'Reset game':
            for client_name in game_data['clients']:
                game_data['clients'][client_name]['attacked_tile'] = None
        else:
            game_data['clients'] = decoded_data

        if len(game_data['clients']) == CONN_LIMIT:
            send_data_to_clients(game_data['clients'], client_name)

    game_data['clients'].pop(client_name, None)
    game_data['sockets'].pop(client_name, None)
    client_socket.close()
