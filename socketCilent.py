import socket
import os
from tdqm import tdqm


def run_client():
    host = "127.0.0.1"
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        print(
            "Connection Successful, \ntype ls for file list, type filename to download"
        )
        choice = input("Enter command")

        client_socket.send(choice.encode())
        response = client_socket.recv(4096).decode()
        print(f"Directory: {response}")
