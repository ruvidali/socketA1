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

```python
elif command.startswith("cp"):
                filename = command.split(" ", 1)[1]
                print(f"\nRequested file: {filename}")

                if os.path.exists(filename):
                    conn.send(b"File found, starting transfer....")

                    filesize = os.path.getsize(filename)
                    conn.send(str(filesize).encode())

                    # Wait for client to be ready
                    conn.recv(1024)

                    bytes_sent = 0
                    with open(filename, "rb") as cf:
                        while bytes_sent < filesize:
                            bytes_read = cf.read(4096)
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

```
Using the command `cp` followed by a filename will start the file transfer process. The process
starts by:
1. Extracting the filename from the command received from the client using the `command.split(" ", 1)[1]`
function. This will split the string using white space(" ") and return the value with index 1
2. Check if the filename extracted exists in the server directory using `os.path.exists(filename)`
3. Find the size of the file using `os.path.getsize(filename)`. This will be used for the chunks and the
progress bar.
4. Send the file using the `open(filename, "rb") as cf`. The "rb" string indicate the mode we want to use
for the transfer. `"r"` is the default which means `open for reading` and `b` means we are reading the
file in binary mode which is required for sending multiple file types
5. Transfer the data in chunks of 4096 bytes until the transfer is complete
6. Send a server response "File does not exist" if the directory check fails

# Client Application - socketClient.py
## Socket Creation
The creation of a socket for the client is similar the server configuration. The client only needs to create
a client socket object using the same host and port details as the server configuration and instead of the
`bind()` function we use the `connect()` function which takes a pair value of host and port as arguments.

```python
def run_client():
    # Define the host and port
    host = "127.0.0.1"
    port = 5000

    # create the client socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Error handling for the connection to the server socket
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(f"Error connecting to the server: {e}")
        sys.exit(1)

    # Print a success message and instructions
    print("Connected to server")
    print("Commands: ls- to list dir, cp <filename> - to download a file, exit\n")

```
Once the client and server are connected the client will receive instructions for the allowed commands.
The program will take the input from the user and check the following:
1. If the user choice is `exit` the program closes
2. If the user choice is `ls`:
  - The client will send the command to the server and wait for a response
  - Response will include of the files in the server directory
3. If the user choice is `cp <filename>`:
  - The client waits for the server to validate the command and check the directory for the file
  - Once the file is found, the server will send confirmation and wait for the `"READY"` response
  from the client
  - The filename is extracted from the server response
  - A received bytes variable is created for progress bar updates
  - Use the `open(f"downloaded_{filename}",) as sf` to create the file in the client directory received the
  data chucks from the server
  - Write the chunks to the open file until the transfer is complete
4. If the filename cannot be found, a server response will be received to notify the user

``` python
while True:
        choice = input("Enter command: ")
        if not choice:
            continue

        if choice.lower() == "exit":
            break

        # Send command to server
        client_socket.send(choice.encode())

        if choice.startswith("cp"): # Check if file exists on server
            response = client_socket.recv(1024).decode()

            if response == "File Exists":
                # Get filesize
                filesize = int(client_socket.recv(1024).decode())

                # Tell server we are ready to receive
                client_socket.send(b"READY")

                # Get the filename and create a variable for the
                # bytes to be received for the progress bar
                filename = choice.split(" ", 1)[1]
                received_bytes = 0

                print(f"Downloading {filename} ({filesize} bytes)...")

                with open(f"downloaded_{filename}", "wb") as sf:
                    while received_bytes < filesize:
                        # Calculate how much to download from the server
                        # Create a variable to only download the chunk size
                        remaining = filesize - received_bytes
                        chunk_size = 4096 if remaining > 4096 else remaining

                        # Receive the data in chunks from the server
                        chunk = client_socket.recv(chunk_size)
                        if not chunk:
                            break

                        # write to the file and update the
                        # received_bytes for the progress bar
                        sf.write(chunk)
                        received_bytes += len(chunk)

                        # Update progress bar
                        draw_progress_bar(received_bytes, filesize)

                # Exit the loop when the file transfer is complete
                # Print the saved filename
                print(f"\nFile saved as: downloaded_{filename}")
            else:
                # Print the server confirmation
                print(f"Server says: {response}")

        else:
            # Print server response for file not found
            response = client_socket.recv(4096).decode()
            print(f"{response}")

    # Close the client socket
    client_socket.close()

```
## Helper Functions
### Progress Bar
A simple progress bar was added for both the server and client to track the transfer progress.

```python
def draw_progress_bar(current, total, bar_length=40):
    # Calculates and prints a manual progress bar to the console
    # Prevent division by zero if file is empty
    if total <= 0:
        return
    fraction = current / total
    arrow = int(fraction * bar_length)
    bar = "█" * arrow + "-" * (bar_length - arrow)
    percent = fraction * 100
    sys.stdout.write(f"\r[{bar}] {percent:.0f}%")
    sys.stdout.flush()
```
The progress bar is designed to take the bytes sent(server) or bytes received(client) and the total filesize
calculate the percentage of its progress.

