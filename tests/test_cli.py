import unittest
from unittest.mock import patch

from password_strength_checker import cli


class TestCLI(unittest.TestCase):
    @patch("password_strength_checker.cli.getpass.getpass", return_value="password")
    @patch("password_strength_checker.cli.check_password_breach")
    @patch("builtins.print")
    @patch("sys.argv", ["password-checker"])
    def test_default_mode_does_not_call_online_service(
        self, mock_print, mock_breach, mock_getpass
    ):
        self.assertEqual(cli.main(), 0)
        mock_breach.assert_not_called()
        mock_getpass.assert_called_once()

    @patch(
        "password_strength_checker.cli.getpass.getpass",
        return_value="synthetic-test-password",
    )
    @patch(
        "password_strength_checker.cli.check_password_breach",
        return_value={"is_pwned": True, "occurrences": 12},
    )
    @patch("builtins.print")
    @patch("sys.argv", ["password-checker", "--check-breach"])
    def test_optional_breach_check_is_called(
        self, mock_print, mock_breach, mock_getpass
    ):
        self.assertEqual(cli.main(), 0)
        mock_breach.assert_called_once_with("synthetic-test-password")


if __name__ == "__main__":
    unittest.main()
