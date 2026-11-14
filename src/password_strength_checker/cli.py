"""Command-line interface for the password checker."""

from __future__ import annotations

import argparse
import getpass

from .analyzer import MAX_PASSWORD_LENGTH, analyze_password
from .breach_checker import BreachCheckError, check_password_breach


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-checker",
        description=(
            "Estimate password guessability locally. "
            "An online breach lookup is optional."
        ),
    )
    parser.add_argument(
        "--check-breach",
        action="store_true",
        help="optionally check HIBP Pwned Passwords using k-anonymity",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    print("=" * 40)
    print("       Password Strength Checker")
    print("=" * 40)
    print("Local analysis is performed offline.")
    password = getpass.getpass("Enter a password to analyze: ")

    try:
        result = analyze_password(password)
    except (TypeError, ValueError) as exc:
        print(f"\nInput error: {exc}")
        return 2

    print("\nPassword Analysis")
    print("-----------------")
    print(f"Score: {result['score']}/4")
    print(f"Strength: {result['strength']}")

    if result["feedback"]:
        print("\nSuggestions:")
        for suggestion in result["feedback"]:
            print(f"- {suggestion}")
    else:
        print("\nNo additional suggestions from the estimator.")

    if args.check_breach:
        if not password:
            print("\nBreach check skipped: the password is empty.")
        else:
            print("\nChecking known breach exposure...")
            try:
                breach_result = check_password_breach(password)
            except BreachCheckError as exc:
                print(f"Breach check unavailable: {exc}")
            else:
                if breach_result["is_pwned"]:
                    print(
                        "Warning: This password appears in known breach data "
                        f"({breach_result['occurrences']:,} occurrences). "
                        "Do not use it."
                    )
                else:
                    print(
                        "No match found in the Pwned Passwords dataset. "
                        "This does not prove the password has never been exposed."
                    )

    print("\nPrivacy and security notes:")
    print("- The local strength analysis does not send the password online.")
    print("- The breach lookup runs only when --check-breach is supplied.")
    print("- The breach lookup sends only a 5-character SHA-1 hash prefix.")
    print("- This estimate is not a guarantee of password security.")
    print(f"- Maximum local analysis length: {MAX_PASSWORD_LENGTH} characters.")

    # Avoid retaining the password in application-level variables longer than
    # necessary. Python strings cannot be reliably zeroed from memory.
    password = None
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
