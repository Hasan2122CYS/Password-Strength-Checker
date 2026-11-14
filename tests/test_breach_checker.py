import hashlib
import io
import unittest
from unittest.mock import patch

from password_strength_checker.breach_checker import (
    BreachCheckError,
    HIBP_RANGE_URL,
    USER_AGENT,
    check_password_breach,
)


class FakeResponse:
    def __init__(self, body: bytes):
        self._body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._body


class TestBreachChecker(unittest.TestCase):
    def setUp(self):
        self.password = "synthetic-test-password-2026"
        self.full_hash = hashlib.sha1(
            self.password.encode("utf-8")
        ).hexdigest().upper()
        self.prefix = self.full_hash[:5]
        self.suffix = self.full_hash[5:]

    @patch("password_strength_checker.breach_checker.urlopen")
    def test_detects_matching_hash_suffix(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(
            f"{self.suffix}:17\r\n".encode("ascii")
        )
        result = check_password_breach(self.password)
        self.assertEqual(
            result,
            {"is_pwned": True, "occurrences": 17},
        )

    @patch("password_strength_checker.breach_checker.urlopen")
    def test_returns_not_found_when_suffix_is_absent(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(b"ABCDEF012345:4\r\n")
        result = check_password_breach(self.password)
        self.assertEqual(
            result,
            {"is_pwned": False, "occurrences": 0},
        )

    @patch("password_strength_checker.breach_checker.urlopen")
    def test_ignores_zero_count_padding_entries(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(
            f"{self.suffix}:0\r\n".encode("ascii")
        )
        result = check_password_breach(self.password)
        self.assertFalse(result["is_pwned"])

    @patch("password_strength_checker.breach_checker.urlopen")
    def test_sends_only_five_character_hash_prefix(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(b"")
        check_password_breach(self.password)

        request = mock_urlopen.call_args.args[0]
        self.assertEqual(request.full_url, f"{HIBP_RANGE_URL}{self.prefix}")
        self.assertNotIn(self.suffix, request.full_url)
        self.assertEqual(request.get_header("User-agent"), USER_AGENT)
        self.assertEqual(request.get_header("Add-padding"), "true")
        self.assertEqual(mock_urlopen.call_args.kwargs["timeout"], 5)

    def test_rejects_empty_password(self):
        with self.assertRaises(ValueError):
            check_password_breach("")

    def test_rejects_non_string_password(self):
        with self.assertRaises(TypeError):
            check_password_breach(None)

    @patch(
        "password_strength_checker.breach_checker.urlopen",
        side_effect=TimeoutError("simulated timeout"),
    )
    def test_wraps_network_errors(self, mock_urlopen):
        with self.assertRaises(BreachCheckError):
            check_password_breach(self.password)


if __name__ == "__main__":
    unittest.main()
