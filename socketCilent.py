import socket
import os
import sys


def run_client():
    host = "127.0.0.1"
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Error handling for connecting to the server
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(f"Error conencting to the server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    while True:
        print("1. Type ls for file list")
        print("2. Type filename to download")
        print("3. Type exit to stop program")
        choice = input("Enter command: ")

        client_socket.send(choice.encode())
        response = client_socket.recv(4096).decode()
        print(f"Directory: {response}")

    client_socket.close()


if __name__ == "__main__":
    run_client()
