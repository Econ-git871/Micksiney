"""Tests for validator module."""

import pytest
from src.validator import is_valid_email, is_positive_integer, sanitize_string


class TestIsValidEmail:
    def test_valid_email(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_email_with_dots(self):
        assert is_valid_email("first.last@example.co.uk") is True

    def test_valid_email_with_plus(self):
        assert is_valid_email("user+tag@example.com") is True

    def test_missing_at_sign(self):
        assert is_valid_email("userexample.com") is False

    def test_missing_domain(self):
        assert is_valid_email("user@") is False

    def test_missing_tld(self):
        assert is_valid_email("user@example") is False

    def test_empty_string(self):
        assert is_valid_email("") is False

    def test_non_string_input(self):
        assert is_valid_email(123) is False
        assert is_valid_email(None) is False

    def test_spaces_in_email(self):
        assert is_valid_email("user @example.com") is False


class TestIsPositiveInteger:
    def test_positive_int(self):
        assert is_positive_integer(1) is True
        assert is_positive_integer(100) is True

    def test_zero(self):
        assert is_positive_integer(0) is False

    def test_negative_int(self):
        assert is_positive_integer(-5) is False

    def test_float(self):
        assert is_positive_integer(1.5) is False

    def test_string(self):
        assert is_positive_integer("1") is False

    def test_none(self):
        assert is_positive_integer(None) is False


class TestSanitizeString:
    def test_normal_string(self):
        assert sanitize_string("hello") == "hello"

    def test_strips_whitespace(self):
        assert sanitize_string("  hello  ") == "hello"

    def test_removes_control_characters(self):
        assert sanitize_string("hello\x00world") == "helloworld"

    def test_removes_newlines_and_tabs(self):
        assert sanitize_string("hello\n\tworld") == "helloworld"

    def test_empty_string(self):
        assert sanitize_string("") == ""

    def test_non_string_raises(self):
        with pytest.raises(TypeError, match="Expected str, got int"):
            sanitize_string(123)

    def test_none_raises(self):
        with pytest.raises(TypeError):
            sanitize_string(None)
