"""Tests for data_store module."""

import pytest
from src.data_store import DataStore


class TestDataStoreBasic:
    def test_set_and_get(self):
        store = DataStore()
        store.set("key", "value")
        assert store.get("key") == "value"

    def test_get_missing_key_returns_default(self):
        store = DataStore()
        assert store.get("missing") is None
        assert store.get("missing", "fallback") == "fallback"

    def test_overwrite_value(self):
        store = DataStore()
        store.set("key", "first")
        store.set("key", "second")
        assert store.get("key") == "second"

    def test_delete_key(self):
        store = DataStore()
        store.set("key", "value")
        store.delete("key")
        assert store.get("key") is None

    def test_delete_missing_key_raises(self):
        store = DataStore()
        with pytest.raises(KeyError, match="Key not found"):
            store.delete("nonexistent")

    def test_set_non_string_key_raises(self):
        store = DataStore()
        with pytest.raises(TypeError, match="Key must be a string"):
            store.set(123, "value")


class TestDataStoreCollections:
    def test_keys_empty(self):
        store = DataStore()
        assert store.keys() == []

    def test_keys_returns_all(self):
        store = DataStore()
        store.set("a", 1)
        store.set("b", 2)
        assert sorted(store.keys()) == ["a", "b"]

    def test_clear(self):
        store = DataStore()
        store.set("a", 1)
        store.set("b", 2)
        store.clear()
        assert len(store) == 0
        assert store.keys() == []


class TestDataStoreDunder:
    def test_len(self):
        store = DataStore()
        assert len(store) == 0
        store.set("a", 1)
        assert len(store) == 1

    def test_contains(self):
        store = DataStore()
        store.set("a", 1)
        assert "a" in store
        assert "b" not in store


class TestDataStoreIntegration:
    """Integration-style tests exercising multiple operations together."""

    def test_set_delete_set_cycle(self):
        store = DataStore()
        store.set("key", "v1")
        store.delete("key")
        store.set("key", "v2")
        assert store.get("key") == "v2"

    def test_clear_then_repopulate(self):
        store = DataStore()
        store.set("a", 1)
        store.clear()
        store.set("b", 2)
        assert "a" not in store
        assert store.get("b") == 2
        assert len(store) == 1

    def test_stores_various_value_types(self):
        store = DataStore()
        store.set("int", 42)
        store.set("list", [1, 2, 3])
        store.set("dict", {"nested": True})
        store.set("none", None)
        assert store.get("int") == 42
        assert store.get("list") == [1, 2, 3]
        assert store.get("dict") == {"nested": True}
        assert store.get("none") is None
