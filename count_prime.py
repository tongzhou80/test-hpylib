from hpylib import spawn, finish, pmap
from math import isqrt
import time

# -------------------------------
# Prime functions
# -------------------------------
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

# Sequential version
def count_primes_seq(start: int, end: int) -> int:
    return sum(is_prime(i) for i in range(start, end))

# Parallel version using pmap
def count_primes_par(start: int, end: int) -> int:
    results = pmap(is_prime, range(start, end))
    return sum(results)

# -------------------------------
# Benchmark
# -------------------------------
if __name__ == "__main__":
    start_num = 1
    end_num = 200000  # small range for demo

    # Sequential
    t0 = time.perf_counter()
    total_seq = count_primes_seq(start_num, end_num)
    t1 = time.perf_counter()
    print(f"Sequential: {total_seq} primes, time = {t1 - t0:.4f} s")

    # Pmap
    t0 = time.perf_counter()
    total_async = count_primes_par(start_num, end_num)
    t1 = time.perf_counter()
    print(f"Pmap: {total_async} primes, time = {t1 - t0:.4f} s")
