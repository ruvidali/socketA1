import socket
import os
from tdqm import tdqm


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
        print(f"Connected to: {addr}")
        while True:
            command = conn.recv(1024).decode()
            if not command:
                break
            # Client should be able to check the directory for the file
            # Or or just type the name of the file to download
            if command == "ls":
                files = os.listdir()
                conn.send(files.encode())
