import sys
import socket
from threading import Thread

# TODO: Change print to Logging

CONN_LIMIT = 2
BUFFER_SIZE = 2048

server_ip = '192.168.1.1'
port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, port))
except socket.error as error:
    print(error)


server_socket.listen(CONN_LIMIT)
print('Waiting for a connection, Server started')


def threaded_client(conn: socket.socket) -> None:
    reply: str
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
            reply = data.decode('utf-8')

            if not data:
                print('Disconnected')
                break
            else:
                print('Received', reply)
                print('Sending', reply)

            conn.sendall(str.encode(reply))
        except:
            break
    
    print('Connection lost')
    conn.close()


while True:
    conn, address = server_socket.accept()
    print('Connected to', address)

    new_client_conn = Thread(target=threaded_client, args=(conn,))
    new_client_conn.start()
