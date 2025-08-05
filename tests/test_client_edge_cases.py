import socket
import pytest

HOST = "127.0.0.1"
PORT = 44445

def test_send_empty_payload():
    with socket.create_connection((HOST, PORT), timeout=2) as s:
        s.sendall(b"")
        s.close()

def test_send_null_bytes():
    with socket.create_connection((HOST, PORT), timeout=2) as s:
        s.sendall(b"alpha\x00\x00\x00")
        data = s.recv(1024)
        assert b"STRING EXISTS" in data or b"STRING NOT FOUND" in data

def test_send_large_payload():
    with socket.create_connection((HOST, PORT), timeout=2) as s:
        s.sendall(b"A" * 5000)
        data = s.recv(1024)
        assert b"STRING" in data

def test_send_binary_junk():
    with socket.create_connection((HOST, PORT), timeout=2) as s:
        s.sendall(b"\x00\xff\xfe\xfa\xfa")
        data = s.recv(1024)
        assert b"STRING" in data or b"DEBUG" in data
