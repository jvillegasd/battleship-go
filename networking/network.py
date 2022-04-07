import socket


BUFFER_SIZE = 2048


class Network:

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = 'localhost'
        self.port = 65432
        self.address = (self.server_ip, self.port)

        self.id = self.connect()
        print(self.id)

    def connect(self) -> None:
        try:
            self.client.connect(self.address)
            return self.client.recv(BUFFER_SIZE).decode()
        except Exception as e:
            print(e)
            pass
# https://www.youtube.com/watch?v=qbL4hPWcnFM&list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq&index=3


n = Network()
