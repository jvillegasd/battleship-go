import threading
from typing import Callable


def thread_safe(function: Callable) -> Callable:
    """
      This decorator makes sure that the decorated
      function is thread safe.
    """

    lock = threading.Lock()

    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            response = function(*args, **kwargs)
        except Exception as error:
            raise error
        finally:
            lock.release()

        return response

    return wrapper
