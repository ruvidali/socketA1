import socket
import os
import sys


def draw_progress_bar(current, total, bar_length=40):
    """Calculates and prints a manual progress bar to the console."""
    fraction = current / total
    arrow = int(fraction * bar_length)
    bar = "█" * arrow + "-" * (bar_length - arrow)
    percent = fraction * 100
    sys.stdout.write(f"\r[{bar}] {percent:.0f}%")
    sys.stdout.flush()


def run_server():
    host = "127.0.0.1"
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started, Listening on host: {host}, port: {port}")

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
                    conn.send(b"File Exists")

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

                    print(f"\n{filename} sent successfully.")
                else:
                    message = f"{filename} does not exist"
                    print(message)
                    conn.send(message.encode())
            else:
                message = f'Command "{command}" not found'
                conn.send(message.encode())

    server_socket.close()


if __name__ == "__main__":
    run_server()
