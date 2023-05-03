from typing import Sequence, Any
from threading import Lock as _Lock


class AtomicInteger(object):
    def __init__(self, n: int):
        self._n: int = n
        self._lock: _Lock = _Lock()

    def get(self) -> int:
        return self._n

    def set(self, n: int):
        self._lock.acquire(True)
        try:
            self._n = n
        finally:
            self._lock.release()

    def _change_and_get(self, d: int) -> int:
        self.set(self.get() + d)
        return self.get()

    def _get_and_change(self, d: int) -> int:
        try:
            return self.get()
        finally:
            self.set(self.get() + d)

    def increment_and_get(self) -> int:
        return self._change_and_get(1)

    def get_and_increment(self) -> int:
        return self._get_and_change(1)

    def decrement_and_get(self) -> int:
        return self._change_and_get(-1)

    def get_and_decrement(self) -> int:
        return self._get_and_change(-1)


def classic_index(obj: Sequence, target: Any) -> int:
    try:
        return obj.index(target)
    except ValueError:
        return -1
