"""Local password guessability analysis powered by zxcvbn."""

from __future__ import annotations

from typing import Any

from zxcvbn import zxcvbn


MAX_PASSWORD_LENGTH = 72

STRENGTH_LEVELS = {
    0: "Very Weak",
    1: "Weak",
    2: "Fair",
    3: "Strong",
    4: "Very Strong",
}


def analyze_password(password: str) -> dict[str, Any]:
    """Estimate password guessability without sending it anywhere.

    The zxcvbn Python implementation documents 72 characters as its default
    maximum and warns against raising that limit due to processing cost.

    Raises:
        TypeError: If password is not a string.
        ValueError: If password is longer than MAX_PASSWORD_LENGTH.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if password == "":
        return {
            "score": 0,
            "strength": STRENGTH_LEVELS[0],
            "feedback": ["Password cannot be empty."],
            "guesses": 1,
        }

    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password exceeds the analysis limit of "
            f"{MAX_PASSWORD_LENGTH} characters."
        )

    result = zxcvbn(password, max_length=MAX_PASSWORD_LENGTH)
    score = result["score"]

    return {
        "score": score,
        "strength": STRENGTH_LEVELS[score],
        "feedback": result.get("feedback", {}).get("suggestions", []),
        "guesses": result.get("guesses"),
    }
