import socket
import threading
from typing import Tuple

HOST = '0.0.0.0'       # Listen on all interfaces
PORT = 44445           # Default port, will later come from config
MAX_PAYLOAD_SIZE = 1024

def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Handles a single client connection."""
    print(f"[+] Connection from {addr}")
    try:
        data = conn.recv(MAX_PAYLOAD_SIZE)
        if not data:
            return
        # Strip null bytes and decode
        query = data.replace(b'\x00', b'').decode('utf-8', errors='ignore')
        print(f"[{addr}] Received: {query}")
        
        # Stub: always respond with STRING EXISTS for now
        response = "STRING EXISTS\n"
        conn.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"[!] Error handling {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection from {addr} closed")

def start_server() -> None:
    """Starts the multithreaded TCP server."""
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