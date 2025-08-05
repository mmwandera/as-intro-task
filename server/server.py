import socket
import threading
from typing import Tuple

HOST = '0.0.0.0'
PORT = 44445
MAX_PAYLOAD_SIZE = 1024


def receive_query(conn: socket.socket) -> str:
    """
    Receives up to MAX_PAYLOAD_SIZE bytes from the client,
    strips null terminators, and decodes to UTF-8.
    """
    raw = conn.recv(MAX_PAYLOAD_SIZE)
    if not raw:
        return ""
    cleaned = raw.replace(b'\x00', b'').decode('utf-8', errors='ignore').strip()
    return cleaned


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Handles a single TCP client connection."""
    print(f"[+] Connection from {addr}")
    try:
        query = receive_query(conn)
        print(f"[{addr}] Received: {query}")

        # Placeholder for future logic
        response = "STRING EXISTS\n"
        conn.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"[!] Error handling {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection from {addr} closed")


def start_server() -> None:
    """Starts a multithreaded TCP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"[*] Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == "__main__":
    start_server()
