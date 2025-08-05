import time
import mmap
import random
import subprocess
import csv
import os
from typing import List, Callable

# Benchmark config
SIZES = [10_000, 50_000, 100_000, 250_000]
QUERIES = ["alpha", "notfound", "foobar", "lastline"]
DATA_DIR = "benchmarks/data"
RESULTS_CSV = "benchmarks/results.csv"


def generate_test_file(num_lines: int, filename: str) -> str:
    """Creates a test file with num_lines and inserts known queries for consistency."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, 'w') as f:
        for _ in range(num_lines - 4):
            f.write(f"{random.randint(100000, 999999)}\n")
        f.write("alpha\n")
        f.write("foobar\n")
        f.write("lastline\n")
        f.write("notfound_marker_line\n")
    return filename


# ------------------------------
# SEARCH ALGORITHM DEFINITIONS
# ------------------------------

def python_in_list(filepath: str, query: str) -> bool:
    with open(filepath, 'r') as f:
        return query in [line.strip() for line in f]


def python_in_set(filepath: str, query: str) -> bool:
    with open(filepath, 'r') as f:
        return query in set(line.strip() for line in f)


def memory_mapped_search(filepath: str, query: str) -> bool:
    with open(filepath, 'r') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            return f"{query}\n".encode() in mm


def grep_subprocess(filepath: str, query: str) -> bool:
    result = subprocess.run(
        ["grep", "-Fxq", query, filepath],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def binary_search_sorted_file(filepath: str, query: str) -> bool:
    with open(filepath, 'r') as f:
        lines = sorted(f.readlines())
    low, high = 0, len(lines) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = lines[mid].strip()
        if mid_val == query:
            return True
        elif mid_val < query:
            low = mid + 1
        else:
            high = mid - 1
    return False


# ------------------------------
# BENCHMARK RUNNER
# ------------------------------

SEARCH_METHODS: List[tuple[str, Callable[[str, str], bool]]] = [
    ("python_in_list", python_in_list),
    ("python_in_set", python_in_set),
    ("memory_mapped", memory_mapped_search),
    ("grep_subprocess", grep_subprocess),
    ("binary_search", binary_search_sorted_file),
]


def benchmark_method(method_name: str, method_fn: Callable, filepath: str, query: str) -> float:
    start = time.perf_counter()
    _ = method_fn(filepath, query)
    end = time.perf_counter()
    return round((end - start) * 1000, 4)


def run_benchmarks():
    with open(RESULTS_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["method", "file_size", "query", "time_ms"])

        for size in SIZES:
            file_path = f"{DATA_DIR}/file_{size}.txt"
            generate_test_file(size, file_path)

            # Pre-sort file for binary search
            with open(file_path, 'r') as f:
                lines = sorted(f.readlines())
            with open(file_path, 'w') as f:
                f.writelines(lines)

            for method_name, method_fn in SEARCH_METHODS:
                for query in QUERIES:
                    time_ms = benchmark_method(method_name, method_fn, file_path, query)
                    writer.writerow([method_name, size, query, time_ms])
                    print(f"{method_name:<20} | {size:>7} rows | query='{query}' | {time_ms:>7} ms")


if __name__ == "__main__":
    run_benchmarks()
