import os
import pytest
from server.searcher import search_in_file, load_file_lines

def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        search_in_file("tests/this_file_does_not_exist.txt", "alpha")

def test_unreadable_file_raises_permission_error(tmp_path):
    restricted = tmp_path / "blocked.txt"
    restricted.write_text("secret\ndata\n")
    os.chmod(restricted, 0)  # Remove all read permissions
    try:
        with pytest.raises(PermissionError):
            load_file_lines(str(restricted))
    finally:
        os.chmod(restricted, 0o644)  # Restore permissions to clean up
