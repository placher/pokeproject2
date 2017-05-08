# Pokeproject 2 : Non-Electric Boogaloo

This repositrory represents the final project for __CSE 30332-01 Programming Paradigms__ completed by

* J. Patrick Lacher (jlacher1@nd.edu)
* John R. Adams (jadams11@nd.edu)

# Installation

This program is run in __python3__ using the __pygame__ and __twisted__ libraries. To install, fork and download the contents of this repository, then ensure that the libraries are installed with the following commands.

    $ git clone https://github.com/placher/pokeproject2
    $ pip3 install pygame
    $ pip3 install twisted
    
If you don't have an instance of __python3__ installed on your machine, you can download a compatable version of it [here](https://www.python.org/downloads/)

# Execution

The game has slightly different runtime arguments for players 1 and 2. Before execution, ensure that the __images__ and __scripts__ folders are in the same directory as the main program.

### Player 1 Execution

Player 1 also serves as the network host, and, thus, must be initialized first.

    $ python3 pokeproject2.py -1 <port to listen on>
    
### Player 2 Execution

Player 2 serves as a network client, and thus needs to be given a host and port with which to connect.

    $ python3 pokeproject2.py -2 <hostname> <port #>
    
# Gameplay

Move your character around using the arrow keys. Use the space bar to launch a projectile towards your opponent. Five clean hits will make you the winner!
