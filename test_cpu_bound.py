import time
from hpylib import async_, finish

def cpu_task(n):
    # CPU-heavy computation
    s = 0
    for i in range(n):
        s += i ** 2
    return s

N = 10_000_000

start = time.time()
for _ in range(4):
    cpu_task(N)
print("CPU-bound tasks (no async-finish):", time.time() - start)

start = time.time()
with finish():
    for _ in range(4):
        async_(lambda: cpu_task(N))
print("CPU-bound tasks (with async-finish):", time.time() - start)
