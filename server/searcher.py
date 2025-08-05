def search_in_file(filepath: str, query: str) -> bool:
    """
    Opens the file and checks for a full-line match with the query string.
    Returns True if the line exactly matches the query, otherwise False.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() == query:
                    return True
        return False
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")