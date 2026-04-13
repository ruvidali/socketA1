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

