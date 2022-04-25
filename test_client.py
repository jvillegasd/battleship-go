from networking.client import Client


host_address = 'localhost'
host_port = 65432

grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, "C", 0, 0, 0, "D", 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, "B", 0, 0, 0, "C", 0, 0, 0, "D", 0, 0, 0, "S", 0, 0, 0, 0],
        [0, 0, 0, "B", 0, 0, 0, "C", 0, 0, 0, "D", 0, 0, 0, "S", 0, 0, 0, 0],
        [0, 0, 0, "B", 0, 0, 0, "C", 0, 0, 0, "D", 0, 0, 0, "S", 0, 0, 0, 0],
        [0, 0, 0, "B", 0, 0, 0, "C", 0, 0, 0, "D", 0, 0, 0, "S", 0, 0, 0, 0],
        [0, 0, 0, "B", 0, 0, 0, "C", 0, 0, 0, 0, 0, 0, 0, "S", 0, 0, 0, 0],
        [0, 0, 0, "B", 0, 0, 0, "C", 0, 0, 0, 0, 0, 0, 0, "S", 0, 0, 0, 0],
        ["R", 0, 0, "B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "S", 0, 0, 0, 0],
        ["R", 0, 0, "B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["R", 0, 0, "B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["R", 0, 0, "B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ["R", 0, 0, "B", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


linkrs = Client('LinkRs', host_address, host_port)
zeldars = Client('ZeldaRs', host_address, host_port)

linkrs.connect_to_server()
zeldars.connect_to_server()


linkrs.lock_ships(grid)
zeldars.lock_ships(grid)

print('Before attack')
print(linkrs.get_game_data())
print(zeldars.get_game_data())


linkrs.attack_enemy_tile((13, 0))
zeldars.attack_enemy_tile((14, 0))


print('After attack')
print(linkrs.get_game_data())
print(zeldars.get_game_data())
