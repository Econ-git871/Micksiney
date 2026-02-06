"""Simple in-memory key-value data store."""


class DataStore:
    """A basic key-value store with get, set, delete, and listing."""

    def __init__(self):
        self._data = {}

    def set(self, key, value):
        """Store a value under the given key.

        Raises:
            TypeError: If key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be a string, got {type(key).__name__}")
        self._data[key] = value

    def get(self, key, default=None):
        """Retrieve the value for the given key, or default if not found."""
        return self._data.get(key, default)

    def delete(self, key):
        """Remove a key from the store.

        Raises:
            KeyError: If the key does not exist.
        """
        if key not in self._data:
            raise KeyError(f"Key not found: {key}")
        del self._data[key]

    def keys(self):
        """Return a list of all keys in the store."""
        return list(self._data.keys())

    def clear(self):
        """Remove all entries from the store."""
        self._data.clear()

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data
