import socket
import threading
from typing import Tuple
import sys
import os

# Fix imports for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.config import extract_linuxpath, get_reread_on_query
from server.searcher import search_in_file, load_file_lines, search_in_memory

HOST = '0.0.0.0'
PORT = 44445
MAX_PAYLOAD_SIZE = 1024

# Load config
try:
    LINUX_PATH = extract_linuxpath()
    REREAD_ON_QUERY = get_reread_on_query()
    print(f"[CONFIG] linuxpath = {LINUX_PATH}")
    print(f"[CONFIG] reread_on_query = {REREAD_ON_QUERY}")
except Exception as e:
    print(f"[ERROR] Failed to load config: {e}")
    exit(1)

# Cache lines once if REREAD_ON_QUERY is False
FILE_LINES = []
if not REREAD_ON_QUERY:
    try:
        FILE_LINES = load_file_lines(LINUX_PATH)
        print(f"[INFO] Cached {len(FILE_LINES)} lines from file")
    except Exception as e:
        print(f"[ERROR] Failed to preload file lines: {e}")
        exit(1)


def receive_query(conn: socket.socket) -> str:
    """
    Receives up to 1024 bytes from client.
    Strips all null bytes and decodes cleanly into a UTF-8 string.
    """
    try:
        raw = conn.recv(1024)  # Hard limit
        if not raw:
            return ""
        cleaned = raw.replace(b'\x00', b'').decode('utf-8', errors='ignore').strip()
        return cleaned
    except Exception as e:
        print(f"[!] Error reading query: {e}")
        return ""


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """
    Handles one client: reads query, checks file, sends result, closes connection.
    """
    print(f"[+] Connection from {addr}")
    try:
        query = receive_query(conn)
        print(f"[{addr}] Received: {query}")

        if REREAD_ON_QUERY:
            found = search_in_file(LINUX_PATH, query)
        else:
            found = search_in_memory(FILE_LINES, query)

        response = "STRING EXISTS\n" if found else "STRING NOT FOUND\n"
        conn.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"[!] Error handling {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection from {addr} closed")


def start_server() -> None:
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