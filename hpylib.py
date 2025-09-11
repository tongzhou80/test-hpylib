# hpylib.py
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from contextlib import contextmanager
import queue

# Global registry for thread groups
_thread_groups = {}
_task_futures = []

_lock = threading.Lock()

def _get_thread_group(name):
    """Get or create a sequential worker for a named thread group."""
    with _lock:
        if name not in _thread_groups:
            # Queue for sequential tasks
            q = queue.Queue()
            
            def worker():
                while True:
                    task = q.get()
                    if task is None:
                        break
                    try:
                        task()
                    except Exception as e:
                        print(f"Task exception: {e}")
                    q.task_done()
            
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            _thread_groups[name] = (q, t)
        return _thread_groups[name]

def async_(fn, thread=None):
    """Submit an async task. If thread is provided, tasks run sequentially in that thread."""
    if thread is None:
        # Run in a regular thread pool (default max_workers = CPU cores)
        pool = ThreadPoolExecutor()
        future = pool.submit(fn)
        _task_futures.append(future)
    else:
        q, _ = _get_thread_group(thread)
        q.put(fn)

@contextmanager
def finish():
    """Context manager: wait for all async tasks to complete."""
    global _task_futures
    try:
        yield
    finally:
        # Wait for all futures
        for f in _task_futures:
            f.result()  # will raise exceptions if any
        _task_futures.clear()
        
        # Wait for all thread-group queues to finish
        for q, t in _thread_groups.values():
            q.put(None)  # sentinel to stop worker
        for q, t in _thread_groups.values():
            t.join()
        _thread_groups.clear()
