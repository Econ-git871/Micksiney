"""Input validation utilities."""

import re


def is_valid_email(email):
    """Check if a string is a valid email address."""
    if not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_positive_integer(value):
    """Check if a value is a positive integer."""
    return isinstance(value, int) and value > 0


def sanitize_string(text):
    """Strip whitespace and remove control characters from a string.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    cleaned = re.sub(r'[\x00-\x1f\x7f]', '', text)
    return cleaned.strip()
