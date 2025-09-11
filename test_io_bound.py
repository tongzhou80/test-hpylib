import os
import time
from hpylib import async_, finish

def write_file_block(filename, block_size=1024*1024*100):
    data = b"x" * block_size
    with open(filename, "ab") as f:
        f.write(data)

N = 5  # number of files
start = time.time()

# Ensure test files are removed
for i in range(N):
    try:
        os.remove(f"file_{i}.bin")
    except FileNotFoundError:
        pass

with finish():
    for i in range(N):
        async_(lambda i=i: write_file_block(f"file_{i}.bin"))

print("Total time (with async-finish):", time.time() - start)


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