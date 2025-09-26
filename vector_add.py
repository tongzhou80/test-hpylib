from hpylib import spawn, finish, pmap
import time

def vector_add_seq(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def vector_add_pmap(a, b):
    return pmap(lambda i: a[i] + b[i], range(len(a)))

def main():
    N = 100_000_000
    a = [1] * N
    b = [1] * N

    # -----------------------
    # Sequential version
    # -----------------------
    start = time.time()
    result = vector_add_seq(a, b)
    print("Total time (sequential):", time.time() - start)

    # -----------------------
    # Async / finish version
    # -----------------------
    start = time.time()
    result1 = vector_add_pmap(a, b)
    print("Total time (parallel):", time.time() - start)
    assert result == result1

if __name__ == "__main__":
    main()