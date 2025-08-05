# server/server.py

import socket
import threading
from typing import Tuple
import sys
import os

# Allow imports to work even when running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.config import extract_linuxpath
from server.searcher import search_in_file

HOST = '0.0.0.0'
PORT = 44445
MAX_PAYLOAD_SIZE = 1024

# Read linuxpath from config
try:
    LINUX_PATH = extract_linuxpath()
    print(f"[CONFIG] linuxpath = {LINUX_PATH}")
except Exception as e:
    print(f"[ERROR] Failed to load linuxpath: {e}")
    exit(1)


def receive_query(conn: socket.socket) -> str:
    """
    Receives the query string from the client and decodes it safely.
    """
    raw = conn.recv(MAX_PAYLOAD_SIZE)
    if not raw:
        return ""
    cleaned = raw.replace(b'\x00', b'').decode('utf-8', errors='ignore').strip()
    return cleaned


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """
    Handles a single client connection: reads the query, searches file,
    sends result, and closes the connection.
    """
    print(f"[+] Connection from {addr}")
    try:
        query = receive_query(conn)
        print(f"[{addr}] Received: {query}")

        found = search_in_file(LINUX_PATH, query)
        response = "STRING EXISTS\n" if found else "STRING NOT FOUND\n"
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
