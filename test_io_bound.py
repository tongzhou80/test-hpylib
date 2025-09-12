import os
import time
from hpylib import spawn, finish

def write_file_block(filename, block_size=1024*1024*100):
    data = b"x" * block_size
    with open(filename, "ab") as f:
        f.write(data)

def main():
    N = 5  # number of files

    # -----------------------
    # Sequential version
    # -----------------------
    start = time.time()
    # Ensure test files are removed
    for i in range(N):
        try:
            os.remove(f"file_{i}.bin")
        except FileNotFoundError:
            pass

    for i in range(N):
        write_file_block(f"file_{i}.bin")
    print("Total time (no async-finish):", time.time() - start)

    # -----------------------
    # Async / finish version
    # -----------------------
    start = time.time()
    # Ensure test files are removed
    for i in range(N):
        try:
            os.remove(f"file_{i}.bin")
        except FileNotFoundError:
            pass

    with finish():
        for i in range(N):
            spawn(write_file_block, f"file_{i}.bin")

    print("Total time (with async-finish):", time.time() - start)

if __name__ == "__main__":
    main()
