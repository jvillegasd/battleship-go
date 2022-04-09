# https://github.com/effiongcharles/network_rock_paper_scissors_game/blob/master/game_client.py
# https://stackoverflow.com/questions/1072821/is-modifying-a-class-variable-in-python-threadsafe

import json
import socket
from threading import Thread


BUFFER_SIZE = 4096

clients_tiles = {}

server_socket = None
host_address = 'localhost'
host_port = 65432


def connect_to_server(client_name: str):
    global server_socket

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host_address, host_port))

        server_thread = Thread(target=server_listener,
                               args=(server_socket, client_name))
        server_thread.start()
    except socket.error as error:
        print(error)


def send_data_to_server(data: object, server_socket: socket.socket):
    message = json.dumps(data)
    server_socket.send(bytes(message, 'utf-8'))


def decode_data(data: bytes) -> object:
    return json.loads(data.decode('utf-8'))


def server_listener(server_socket: socket.socket, client_name: str):
    global clients_tiles

    send_data_to_server(client_name, server_socket)
    data = server_socket.recv(BUFFER_SIZE)
    ack = decode_data(data)
    
    print('Server ACK:', ack)

    while True:
        data = server_socket.recv(BUFFER_SIZE)
        if not data:
            break

        decoded_data = decode_data(data)
        print('received_data', decoded_data)
        clients_tiles = decoded_data

    server_socket.close()


connect_to_server('LinkRs')