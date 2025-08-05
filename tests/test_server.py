import os
import socket
import pytest
from server.config import extract_linuxpath, get_reread_on_query
from server.searcher import (
    search_in_file,
    search_in_memory,
    load_file_lines
)

TEST_FILE = "tests/test_data.txt"
TEST_CONFIG = "tests/test_settings.conf"

# ----------------------------
# Test File Setup and Teardown
# ----------------------------

@pytest.fixture(scope="module", autouse=True)
def setup_test_files():
    # Test search file
    with open(TEST_FILE, "w") as f:
        f.write("alpha\nbeta\ngamma\n")
    # Test config
    with open(TEST_CONFIG, "w") as f:
        f.write("linuxpath=tests/test_data.txt\n")
        f.write("reread_on_query=True\n")
    yield
    os.remove(TEST_FILE)
    os.remove(TEST_CONFIG)

# ---------------------
# Config Parsing Tests
# ---------------------

def test_extract_linuxpath_valid():
    path = extract_linuxpath(TEST_CONFIG)
    assert path == TEST_FILE

def test_get_reread_on_query_true():
    assert get_reread_on_query(TEST_CONFIG) is True

def test_get_reread_on_query_default_true(tmp_path):
    config_path = tmp_path / "default.conf"
    config_path.write_text("irrelevant_key=value\n")
    assert get_reread_on_query(str(config_path)) is True

# ---------------------
# File Search Logic
# ---------------------

def test_search_in_file_hit():
    assert search_in_file(TEST_FILE, "alpha") is True

def test_search_in_file_miss():
    assert search_in_file(TEST_FILE, "not_in_file") is False

def test_search_in_memory_hit():
    lines = load_file_lines(TEST_FILE)
    assert search_in_memory(lines, "gamma") is True

def test_search_in_memory_miss():
    lines = load_file_lines(TEST_FILE)
    assert search_in_memory(lines, "notfound") is False

# ---------------------
# Payload / Socket Tests
# ---------------------

def test_socket_open_and_close():
    try:
        s = socket.create_connection(("127.0.0.1", 44445), timeout=2)
        s.close()
        assert True
    except Exception:
        pytest.fail("Socket failed to open or close cleanly")

def test_socket_sends_null_bytes():
    """Server should handle null bytes and respond."""
    try:
        with socket.create_connection(("127.0.0.1", 44445), timeout=2) as s:
            s.sendall(b"alpha\x00\x00")
            data = s.recv(1024)
            assert b"STRING EXISTS" in data
    except Exception:
        pytest.fail("Server crashed or failed on null byte payload")

def test_socket_sends_empty_payload():
    """Sending nothing should not crash the server."""
    try:
        with socket.create_connection(("127.0.0.1", 44445), timeout=2) as s:
            s.sendall(b"")
            s.close()
    except Exception:
        pytest.fail("Server crashed on empty input")
