from networking.client import Client


host_address = 'localhost'
host_port = 65432


client = Client('LinkRs', host_address, host_port)
client.connect_to_server()
client.send_data_to_server({'hello': 'world'})
client.send_data_to_server({'hello': 'world2'})

