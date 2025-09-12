# hpylib/__init__.py
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from contextlib import contextmanager
import itertools
import os

# -------------------------
# Configuration / pool
# -------------------------
mp_or_mt = os.environ.get("HPYLIB_MODE", "mp")  # default to "mp"
_pool = None

def _get_pool():
    """Lazy initialization of the pool."""
    global _pool
    if _pool is None:
        if mp_or_mt == "mp":
            _pool = ProcessPoolExecutor()
        elif mp_or_mt == "mt":
            _pool = ThreadPoolExecutor()
        else:
            raise ValueError(f"Invalid value for mp_or_mt: {mp_or_mt}. Use 'mp' or 'mt'.")
    return _pool

_task_futures = []

# -------------------------
# Async / spawn
# -------------------------
def async_(fn, *args, **kwargs):
    """Submit a task to run asynchronously in the pool, with optional args/kwargs."""
    future = _get_pool().submit(fn, *args, **kwargs)
    _task_futures.append(future)
    return future

# Alias
spawn = async_

# -------------------------
# Finish context manager
# -------------------------
@contextmanager
def finish():
    """Context manager: wait for all async tasks submitted inside the block."""
    try:
        yield
    finally:
        for f in _task_futures:
            f.result()  # raises exception if any
        _task_futures.clear()

# -------------------------
# Top-level pmap worker
# -------------------------
def _pmap_worker(chunk, fn):
    """Top-level worker function for pmap (picklable)."""
    return [fn(x) for x in chunk]

# -------------------------
# Parallel map
# -------------------------
def pmap(fn, iters):
    """
    Parallel map: apply fn to each element of iters in parallel.
    Blocking call. Returns list of results.
    """
    pool = _get_pool()
    n_workers = pool._max_workers
    iters = list(iters)
    n = len(iters)
    if n == 0:
        return []

    chunk_size = (n + n_workers - 1) // n_workers  # ceil division
    chunks = [iters[i:i + chunk_size] for i in range(0, n, chunk_size)]

    futures = [pool.submit(_pmap_worker, chunk, fn) for chunk in chunks]
    results = list(itertools.chain.from_iterable(f.result() for f in futures))
    return results
