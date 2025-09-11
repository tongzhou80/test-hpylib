# hpylib.py
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import itertools

# Global thread pool and list of futures
_pool = ThreadPoolExecutor()
_task_futures = []


def async_(fn):
    """Submit a task to run asynchronously in the thread pool."""
    global _task_futures
    future = _pool.submit(fn)
    _task_futures.append(future)
    return future


# Alias for async_
spawn = async_


@contextmanager
def finish():
    """Context manager: wait for all async tasks submitted inside the block."""
    global _task_futures
    try:
        yield
    finally:
        # Wait for all submitted tasks to finish
        for f in _task_futures:
            f.result()  # raises exception if any
        # Clear the list for the next finish block
        _task_futures.clear()


def pmap(fn, iters):
    """
    Parallel map: apply fn to each element of iters in parallel.
    Blocking call. Returns list of results.
    """
    n_workers = _pool._max_workers
    iters = list(iters)
    n = len(iters)
    chunk_size = (n + n_workers - 1) // n_workers  # ceil division

    # Divide the work into chunks
    chunks = [iters[i:i + chunk_size] for i in range(0, n, chunk_size)]

    # Submit one chunk per worker
    futures = [_pool.submit(lambda chunk=chunk: [fn(x) for x in chunk]) for chunk in chunks]

    # Flatten results in the original order
    results = list(itertools.chain.from_iterable(f.result() for f in futures))
    return results
