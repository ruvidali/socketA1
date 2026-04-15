# CS310 Assignment 1
# Created by Students
# Lebeshiivah Paige Otto - S11199911
# Alfred Samuela - S11079049

import socket
import os
import sys


def draw_progress_bar(current, total, bar_length=40):
    # Calculates and prints a manual progress bar to the console
    fraction = current / total
    arrow = int(fraction * bar_length)
    bar = "█" * arrow + "-" * (bar_length - arrow)
    percent = fraction * 100
    sys.stdout.write(f"\r[{bar}] {percent:.0f}%")
    sys.stdout.flush()


def run_server():
    # define the host and port
    host = "127.0.0.1"
    port = 5000

    # create the server socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the host and port values to the socket object
    server_socket.bind((host, port))

    # enable the server to accept 1 connection
    server_socket.listen(1)

    # print a connection success message
    print(f"Server started, Listening on host: {host}, port: {port}")

    # Get the client address
    conn, addr = server_socket.accept()
    # Use a with statement for the client connection
    with conn:
        # Print the clent address
        print(f"Client Connected: {addr}")
        while True:
            # While the connection is active wait for data
            data = conn.recv(1024)
            if not data:
                break

            # Decode the client data
            command = data.decode()

            # Process for the ls command
            # List the server directory files
            # Send the list result to the client
            if command == "ls":
                files = os.listdir()
                conn.send("\n".join(files).encode())
                print("Directory list sent")

            # Process for the cp command
            # 1.Extract the filename from the command
            # 2.Check if the file exists
            # 3.If the file exists:
            # a.Send confirmation to the client
            elif command.startswith("cp"):
                filename = command.split(" ", 1)[1]
                print(f"\nRequested file: {filename}")

                # Check if the filename in the command exists in
                # the server directory
                if os.path.exists(filename):
                    response = "File Exists"
                    conn.send(response.encode())

                    # check the filesize and send it to the client
                    filesize = os.path.getsize(filename)
                    conn.send(str(filesize).encode())

                    # Wait for client to be ready
                    conn.recv(1024)
                    print("Client Ready for transfer")

                    # create a variable to track the bytes sent
                    bytes_sent = 0
                    # use a with statement for the file transfer
                    # Open the target file and read the bytes ("rb")
                    with open(filename, "rb") as cf:
                        # Use a while loop to send the file to the client
                        # unit all the bytes have been sent
                        while bytes_sent < filesize:
                            # read the file in chunks of 4096
                            bytes_read = cf.read(4096)
                            if not bytes_read:
                                break
                            # send the file bytes to the client socket
                            conn.sendall(bytes_read)

                            # track the bytes sent for the progress bar
                            bytes_sent += len(bytes_read)
                            # Call the progress bar function
                            draw_progress_bar(bytes_sent, filesize)

                    # print success message
                    print("Download complete\n File transfer successful")
                else:
                    # else statement for a invalid file request to
                    # be sent to the client
                    message = "File does not exist"
                    print(message)
                    conn.send(message.encode())
            else:
                # else statement for an invalid command
                message = f'Command "{command}" not found'
                conn.send(message.encode())

    # close the server socket
    server_socket.close()


if __name__ == "__main__":
    run_server()
