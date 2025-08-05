from typing import List


def search_in_file(filepath: str, query: str) -> bool:
    """Searches the file line-by-line for an exact match of the query string."""
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


def load_file_lines(filepath: str) -> List[str]:
    """Loads the file into a list of stripped lines (for caching)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


def search_in_memory(lines: List[str], query: str) -> bool:
    """Searches an in-memory list of lines for an exact match."""
    return query in lines