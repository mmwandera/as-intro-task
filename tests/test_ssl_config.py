import pytest

def test_ssl_config_true(tmp_path):
    config_path = tmp_path / "ssl_on.conf"
    config_path.write_text("use_ssl=True\n")
    lines = config_path.read_text().splitlines()
    assert any("use_ssl=True" in line for line in lines)

def test_ssl_config_false(tmp_path):
    config_path = tmp_path / "ssl_off.conf"
    config_path.write_text("use_ssl=False\n")
    lines = config_path.read_text().splitlines()
    assert any("use_ssl=False" in line for line in lines)
