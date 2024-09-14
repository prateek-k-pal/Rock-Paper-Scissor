# Rock-Paper-Scissors

## Over HTTP

This is a basic Rock-Paper-Scissors game made with the Pygame library and Python. The game has a [Server](./server.py) component that can be used to run a Python server, which communicates over the HTTP protocol with the [Client](./client.py) file. This client file can be run on a local machine if you have a Python interpreter installed with Pygame, Flask and Dotenv modules present. Just create an `.env` file with the server IP/URL (given below). Replace the IP below with the actual one. To run the program locally use 3 terminals - One Server, Two Clients and `localhost` in the place of URL/IP.

```
SERVER_URL="192.168.1.1"
```

If you just want to enjoy the game, download and run the [Source.exe](./dist/source.exe) file present in [dist](./dist/) folder. Input the URL without `https://` when asked and press ENTER.

## Over TCP

Another version of the game is present in the folder [Using_TCP](./Using_TCP/), using the TCP protocol to run communications between the client and the server. It can be set up over a working Python TCP server. To run the program locally use 3 terminals - One Server, Two Clients. You should also have Pygame and pickle module installed.

### Disclaimer

**Important**: This game is intended for development and testing purposes only. It is not designed to ensure the security or safety of information transmitted over the internet. Users should be aware of the following:

- **Security Risks**: As this game communicates over HTTP and is intended for local or development use, it does not guarantee secure transmission of data. Sensitive or personal information should not be shared or transmitted through this application.

- **Development Use Only**: This application is a prototype and may have vulnerabilities or limitations. It should not be used in a production environment where security and data integrity are critical.
