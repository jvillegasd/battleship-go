# https://www.youtube.com/watch?v=_fx7FQ3SP0U&list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq&index=1

import sys
import socket
from threading import Thread

# Change print to Logging

CONN_LIMIT = 2
server_ip = ''
port = 5555

server_socket = socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, port))
except socket.error as error:
    print(error)


server_socket.listen(CONN_LIMIT)
print('Waiting for a connection, Server started')

def threaded_client(conn):
  pass

while True:
  conn, address = server_socket.accept()
  print('Connected to', address, type(conn))
  
  new_client_conn = Thread(target=threaded_client, args=(conn,))
  new_client_conn.start()
# https://www.youtube.com/watch?v=_whymdfq-R4&list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq&index=2