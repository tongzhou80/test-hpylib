import time
from hpylib import async_, finish

def cpu_task(n):
    # CPU-heavy computation
    s = 0
    for i in range(n):
        s += i ** 2
    return s

def main():
    N = 20_000_000

    # Sequential execution
    start = time.time()
    for _ in range(4):
        cpu_task(N)
    print("CPU-bound tasks (no async-finish):", time.time() - start)

    # Async / finish execution
    start = time.time()
    with finish():
        for _ in range(4):
            async_(cpu_task, N)
    print("CPU-bound tasks (with async-finish):", time.time() - start)

if __name__ == "__main__":
    main()
