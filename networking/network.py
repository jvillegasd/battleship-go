import json


class Network:
    """ This class handles networking common logic. """

    def create_datagram(self, buffer_size: int, data: object) -> bytes:
        """ This function creates a datagram of fixed length. """

        message = json.dumps(data)
        header_size = abs(buffer_size - len(message))
        datagram = f'{"":*>{header_size}}' + message

        return bytes(datagram, 'utf-8')

    def decode_data(self, data: bytes) -> object:
        """ This function decode data received from server. """

        decoded_data = data.decode('utf-8')
        cleaned_data = decoded_data.replace('*', '')

        return json.loads(cleaned_data)
