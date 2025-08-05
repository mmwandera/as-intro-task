from typing import Optional


def extract_linuxpath(config_path: str = "configs/settings.conf") -> Optional[str]:
    """
    Reads the config file and extracts the linuxpath entry.
    Ignores all unrelated lines.
    """
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith("linuxpath="):
                    return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to parse config: {e}")
    
    raise ValueError("linuxpath= not found in config file.")
