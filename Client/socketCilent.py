import socket
import sys


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


def run_client():
    # Define the host and port
    host = "127.0.0.1"
    port = 5000

    # create the client socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Error handling for the coonection to the server socket
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(f"Error connecting to the server: {e}")
        sys.exit(1)

    # Print a success message and intructions
    print("Connected to server")
    print("Commands: ls- to list dir, cp <filename> - to download a file, exit\n")

    # While loop once the client has succesfully connected to the
    # server
    while True:
        choice = input("Enter command: ")
        if not choice:
            continue

        if choice.lower() == "exit":
            break

        # Send command to server
        client_socket.send(choice.encode())

        if choice.startswith("cp"):
            # Check if file exists on server
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


if __name__ == "__main__":
    run_client()
