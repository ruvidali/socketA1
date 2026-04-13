import socket
import os
import sys


def draw_progress_bar(current, total, bar_length=40):
    """Calculates and prints a manual progress bar to the console."""
    # Prevent division by zero if file is empty
    if total <= 0:
        return
    fraction = current / total
    arrow = int(fraction * bar_length)
    bar = "█" * arrow + "-" * (bar_length - arrow)
    percent = fraction * 100
    sys.stdout.write(f"\r[{bar}] {percent:.0f}%")
    sys.stdout.flush()


def run_client():
    host = "127.0.0.1"
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(f"Error connecting to the server: {e}")
        sys.exit(1)

    print("Connected to server")
    print("Commands: ls, cp <filename>, exit\n")

    while True:
        choice = input("Enter command: ")
        if not choice:
            continue

        if choice.lower() == "exit":
            break

        # Send command to server
        client_socket.send(choice.encode())

        if choice.startswith("cp"):
            # 1. Check if file exists on server
            response = client_socket.recv(1024).decode()

            if response == "EXISTS":
                # 2. Get filesize
                filesize = int(client_socket.recv(1024).decode())

                # 3. Tell server we are ready to receive (the "speed bump")
                client_socket.send(b"READY")

                filename = choice.split(" ", 1)[1]
                received_bytes = 0

                print(f"Downloading {filename} ({filesize} bytes)...")

                with open(f"downloaded_{filename}", "wb") as f:
                    while received_bytes < filesize:
                        # Calculate how much to read (don't read more than needed)
                        remaining = filesize - received_bytes
                        chunk_size = 4096 if remaining > 4096 else remaining

                        chunk = client_socket.recv(chunk_size)
                        if not chunk:
                            break

                        f.write(chunk)
                        received_bytes += len(chunk)

                        # Update progress bar
                        draw_progress_bar(received_bytes, filesize)

                print(f"\n[+] File saved as: downloaded_{filename}")
            else:
                print(f"Server says: {response}")

        else:
            # Handle standard commands like 'ls'
            response = client_socket.recv(4096).decode()
            print(f"Response:\n{response}")

    client_socket.close()


if __name__ == "__main__":
    run_client()

