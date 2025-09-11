# hpylib.py
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

# Global thread pool and list of futures
_pool = ThreadPoolExecutor()
_task_futures = []

def async_(fn):
    """Submit a task to run asynchronously in the thread pool."""
    global _task_futures
    future = _pool.submit(fn)
    _task_futures.append(future)

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
