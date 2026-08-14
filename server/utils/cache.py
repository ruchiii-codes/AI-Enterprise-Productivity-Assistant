import time
from typing import Any


class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._cache.get(key)

        if entry is None:
            return None

        value, timestamp = entry

        if time.time() - timestamp >= self.ttl_seconds:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.time())

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()

    def __len__(self) -> int:
        return len(self._cache)