import time

from server.utils.cache import TTLCache


def test_cache_set_and_get():
    cache = TTLCache(ttl_seconds=10)

    cache.set("test", "hello")

    assert cache.get("test") == "hello"


def test_cache_returns_none_for_missing_key():
    cache = TTLCache(ttl_seconds=10)

    assert cache.get("missing") is None


def test_cache_expires():
    cache = TTLCache(ttl_seconds=0.1)

    cache.set("test", "hello")

    assert cache.get("test") == "hello"

    time.sleep(0.15)

    assert cache.get("test") is None


def test_cache_delete():
    cache = TTLCache(ttl_seconds=10)

    cache.set("test", "hello")
    cache.delete("test")

    assert cache.get("test") is None


def test_cache_clear():
    cache = TTLCache(ttl_seconds=10)

    cache.set("one", 1)
    cache.set("two", 2)

    cache.clear()

    assert len(cache) == 0