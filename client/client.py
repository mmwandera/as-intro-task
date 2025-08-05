import socket

def send_query(query: str):
    with socket.create_connection(("127.0.0.1", 44445)) as sock:
        sock.sendall(query.encode('utf-8'))
        response = sock.recv(1024)
        print("Server response:", response.decode().strip())

if __name__ == "__main__":
    send_query("test_string")
