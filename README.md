# Socket Programming
## CS310 Assignment 1 - Python socket application

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
## Socket Creation
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

### socket.socket(family,type,proto,fileno)
The socket function takes four arguments family, type, proto and fileno. We are
only using `family` and `type`. The default value for `family` is `AF_INET`. This 
require a pair of values (host, port) where the host represents a hostname or
an IPV4 address and port is an integer for an available port.
```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

### socket.bind(address)
The host and port values are `127.0.0.1` and `5000`. The bind function takes the
pair values and binds it socket object. The socket must not be bound already.
```python
server_socket.bind((host,port))
```

### listen([backlog])
After binding the address to the socket object we need to enable the server to
accept connections. This creates a "waiting room" for client connections and the
number of allowed users in the waiting room before the function starts refusing
new connections is the backlog argument which is an integer.

```python
server_socket.listen(1)
```
This code indicates a backlog of 1 client allowed in the waiting room.

### socket.accept()
 The `accept()` function returns a pair value of (conn, address) when a 
 bounded socket accepts a connection.
```python
conn, addr = server_socket.accept()
```
This code saves the client socket object to be able to send and receive
data and an address bound to the client socket object

## The Connection

```python
conn, addr = server_socket.accept()
    with conn:
        print(f"Client Connected: {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode()

            if command == "ls":
                files = os.listdir()
                conn.send("\n".join(files).encode())

            elif command.startswith("cp"):
                filename = command.split(" ", 1)[1]
                print(f"\nRequested file: {filename}")

                if os.path.exists(filename):
                    conn.send(b"File found, starting transfer....")

                    filesize = os.path.getsize(filename)
                    conn.send(str(filesize).encode())

                    # Wait for client to be ready (prevents buffer overlap)
                    conn.recv(1024)

                    bytes_sent = 0
                    with open(filename, "rb") as f:
                        while bytes_sent < filesize:
                            bytes_read = f.read(4096)
                            if not bytes_read:
                                break
                            conn.sendall(bytes_read)

                            bytes_sent += len(bytes_read)
                            # Call our manual progress bar function
                            draw_progress_bar(bytes_sent, filesize)

                    print("Download complete\n File transfer successful")
                else:
                    message = "File does not exist"
                    print(message)
                    conn.send(message.encode())
            else:
                message = f'Command "{command}" not found'
                conn.send(message.encode())


```
The socket server has three main functions:
1. Check the server directory file list using the command `ls`
2. Download an available file from the server directory using the command `cp <filename>`
3. The server will automatically close when the client terminates the connection with `exit`

### List directory
The `ls` command will utilise the os module to access operating system functionality like 
opening files, process management and manipulating paths. The ls command implements a 
similar function as the bash ls command which prints a list of file or directories in a 
path.

```python
data = conn.recv(1024)
            if not data:
                break

command = data.decode()

            if command == "ls":
                files = os.listdir()
                conn.send("\n".join(files).encode())

```
Incoming data is decoded and saved in the command variable. If the command is equal to `ls`,
the `os.listdir()` function will return a list of files in the current working directory of
the server. The result is saved to a variable called command and is sent back to the client
as a response

### Download File
The client can send the command `cp <filename>` where filename is a file that exists in the
working directory of the python server application.


