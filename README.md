# Battleship Go

Battleship Go is a multiplayer battleship game made in Python using Pygame. Multiplayer uses sockets for connection under the Client-Server architecture.


## Stages

This project was made using a simple state machine logic and it is represented as stages. The stages are:

 - Lobby: Connect to game server and waits untils all players are ready.
 - Ship lock: Move and rotate your ships before battle starts.
 - Battle: Guess where the enemy's ships are and sink them all.
 - Game finished: Shows who is the winner and start a new game.

## GUI

This project does not uses any third-party library, every GUI item was hand-crafted.

## Sprites

Sprites used in this project are not my authorship. There were found on internet, credits are shown below:

 - [Water+](https://ninjikin.itch.io/water): Map was created using these assets.
 - [Sea Warfare set](https://opengameart.org/content/sea-warfare-set-ships-and-more)

## Images