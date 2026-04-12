import socket
import os
import sys


def run_server():
    # Server setup
    host = "127.0.0.1"
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Sever started, Listening on host: {host}, port: {port}")

    conn, addr = server_socket.accept()
    with conn:
        print(f"User Connected: {addr}")
        while True:
            command = conn.recv(1024).decode().lower()
            if not command:
                break
            # Client should be able to check the directory for the file
            # Or or just type the name of the file to download
            if command == "ls":
                files = os.listdir()
                print(files)
                conn.send("\n".join(files).encode())
            elif command.startswith("cp"):
                print("Exiting Program\n")
                sys.exit(1)

    server_socket.close()


if __name__ == "__main__":
    run_server()
