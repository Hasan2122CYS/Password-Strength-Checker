"""Optional Have I Been Pwned Pwned Passwords range lookup."""

from __future__ import annotations

import hashlib
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/"
USER_AGENT = "Password-Strength-Checker/1.0"
REQUEST_TIMEOUT_SECONDS = 5


class BreachCheckError(RuntimeError):
    """Raised when the remote breach lookup cannot be completed safely."""


def check_password_breach(password: str) -> dict[str, int | bool]:
    """Check whether a password appears in HIBP Pwned Passwords.

    The password is hashed locally using SHA-1 for the API's range protocol.
    Only the first five hexadecimal hash characters are sent. The remaining
    hash comparison happens locally. SHA-1 here is not used for password
    storage, authentication, or password hashing.

    Returns:
        {"is_pwned": bool, "occurrences": int}

    Raises:
        TypeError: If password is not a string.
        ValueError: If password is empty.
        BreachCheckError: If the request or response cannot be processed.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if password == "":
        raise ValueError("Password cannot be empty.")

    full_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = full_hash[:5], full_hash[5:]

    request = Request(
        url=f"{HIBP_RANGE_URL}{prefix}",
        headers={
            "User-Agent": USER_AGENT,
            "Add-Padding": "true",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("ascii")
    except (HTTPError, URLError, TimeoutError, OSError, UnicodeDecodeError) as exc:
        raise BreachCheckError(
            "The breach lookup could not be completed. "
            "Your local password analysis is still available."
        ) from exc

    for line in body.splitlines():
        try:
            returned_suffix, raw_count = line.strip().split(":", 1)
            count = int(raw_count)
        except (ValueError, TypeError):
            continue

        if count > 0 and returned_suffix.upper() == suffix:
            return {"is_pwned": True, "occurrences": count}

    return {"is_pwned": False, "occurrences": 0}
