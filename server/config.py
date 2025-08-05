from typing import Optional


def extract_linuxpath(config_path: str = "configs/settings.conf") -> Optional[str]:
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith("linuxpath="):
                    return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    raise ValueError("linuxpath= not found in config file.")


def get_reread_on_query(config_path: str = "configs/settings.conf") -> bool:
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if line.startswith("reread_on_query="):
                    return line.split("=", 1)[1].strip().lower() == "true"
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    return True  # Default to True if not specified