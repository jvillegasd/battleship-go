from networking.client import Client


client = Client('LinkRs', 'localhost', 65432)
client.connect_to_server()
client.send_data_to_server('Testing this function')
client.send_data_to_server({'LinkRs': {'attacked_tile': [5, 5]}})