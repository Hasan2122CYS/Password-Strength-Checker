# Password Strength Checker

An offline-first command-line password analysis tool. It estimates password
guessability locally with `zxcvbn` and offers an optional Have I Been Pwned
Pwned Passwords lookup using the k-anonymity range API.

> **Important:** A score is an estimate, not a security guarantee. Do not use
> this project as a replacement for a production authentication system,
> password hashing, MFA, rate limiting, or security review.

## Features

- Local password guessability estimation with `zxcvbn` (score 0–4).
- Human-readable strength labels and estimator feedback.
- Hidden terminal input via `getpass`.
- Offline by default; no network request during normal analysis.
- Optional compromised-password lookup with `--check-breach`.
- Privacy-preserving HIBP range lookup: the password is hashed locally and
  only the first five hexadecimal characters of its SHA-1 hash are sent.
  The returned suffixes are compared locally.
- `Add-Padding: true` is requested to reduce response-size information leakage.
- Explicit input validation and a 72-character analysis limit, matching the
  documented default limit of the Python `zxcvbn` implementation.
- Automated unit tests, including tests that mock network access.

## Requirements

- Python 3.10 or newer.
- `zxcvbn==4.5.0` (pinned in `requirements.txt`).

## Setup on Windows PowerShell

From the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

If PowerShell blocks activation, use this for the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Run

Offline analysis (default):

```powershell
python -m password_strength_checker
```

Optional online compromised-password lookup:

```powershell
python -m password_strength_checker --check-breach
```

The online lookup is never performed unless the explicit flag is supplied.
The command-line input is hidden while typing.

You can also use the installed command:

```powershell
password-checker
password-checker --check-breach
```

## Tests

Run the full test suite:

```powershell
python -m unittest discover -s tests -v
```

The breach-check tests mock the HTTP request; running the test suite does not
send passwords or test data to the internet.

## Architecture

```text
Password-Strength-Checker/
├── src/
│   └── password_strength_checker/
│       ├── __init__.py
│       ├── __main__.py
│       ├── analyzer.py
│       ├── breach_checker.py
│       └── cli.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_breach_checker.py
│   └── test_cli.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Privacy and security

### Local analysis

The password is passed to the local `zxcvbn` estimator. The application does
not intentionally save, print, or transmit the password during local analysis.
Python cannot guarantee secure zeroization of immutable strings in memory.

### Optional breach lookup

When `--check-breach` is enabled:

1. The application calculates a SHA-1 digest locally, using UTF-8 encoding.
2. It sends only the first five hexadecimal characters to the HIBP Pwned
   Passwords range endpoint.
3. HIBP returns matching hash suffixes and occurrence counts.
4. The application compares the full hash suffix locally.

SHA-1 is used here only because it is the format required by this lookup
protocol. It is **not** used to store passwords or authenticate users.
The password itself and its complete hash are not sent to HIBP.

The lookup requires an internet connection. If it fails, the local analysis
remains available. A "no match" result means only that no match was found in
the dataset queried; it is not proof that a password has never been exposed.

## Limitations

- `zxcvbn` is a guessability estimator, not a password verifier and not a
  cryptographic proof of strength.
- Its built-in dictionaries and pattern models may not recognize every
  language, cultural pattern, or organization-specific term.
- The 72-character limit is a deliberate resource-protection boundary for
  this estimator. It is not a universal password-length policy.
- The breach dataset may not contain every compromised password.
- The application does not create accounts, store passwords, hash passwords
  for authentication, or enforce login rate limits.

## References

- [zxcvbn Python implementation](https://github.com/dwolfhub/zxcvbn-python)
- [Have I Been Pwned – Pwned Passwords API](https://haveibeenpwned.com/api/v3)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

## License

MIT. See [LICENSE](LICENSE).
