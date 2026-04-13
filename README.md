# Socket Programming
## Assignment 1 - Python socket application

### Setup for using the client and server
1. Clone the repository
```bash
git clone https://github.com/ruvidali/socketA1.git
```
2. Add test files to the Server folder
3. Run the server program
```bash
python socketServer.py
```
4. Run the client program
```bash
python socketClient.py
```

### Client Instructions
The client has 3 main commands for interacting with the server:
1. Check files in the server directory with the __ls__ command
2. Download an available file from the server directory using __cp \<filename\>__
3. Exit the program with the command __exit__

# Server Application - socketServer.py
The server application for this assignment uses 3 imports: socket, os and sys. 
The socket library holds all the necessary functions for implementing sockets 
your ideal implementation. We have chosen TCP as our transport mechanism 
because of its reliability. The server code has a main `run_server()` that holds
the main functionality for this assignment.

```python
def run_server():
    host = "127.0.0.1"
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started, Listening on host: {host}, port: {port}")

    conn, addr = server_socket.accept()

```
This section of the code initializes the socket to use `AF_INET - IPV4` and
`SOCK_STREAM - TCP`. The following functions are essential for running a python
socket application:
1. socket()
2. bind()
3. listen()
4. accept()
5. send()
6. close()

## socket()
The socket function takes four arguments family, type, proto and fileno. We are
only using `family` and `type`. The default value for `family` is `AF_INET`. This 
require a pair of values (host, port) where the host represents a hostname or
an IPV4 address and port is an integer for an available port.
```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

## bind()
The host and port values are `127.0.0.1` and `5000`. The bind function takes the
pair values and binds it socket object. The socket must not be bound already.
```python
server_socket.bind((host,port))
```

## listen()
After binding the address to the socket object we need to enable the server to
accept connections. This creates a "waiting room" for client connections and the
number of allowed users in the waiting room before the function starts declining
connections is the backlog argument which is an integer.

```python
server_socket.listen(1)
```
This code indicates a backlog of 1 client allowed in the waiting room.


