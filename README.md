# Password Strength Checker

A simple Python project that evaluates password strength using basic security criteria.

## Features

- Checks password length.
- Detects uppercase and lowercase letters.
- Detects numbers and special characters.
- Classifies passwords as Weak, Medium, or Strong.
- Provides suggestions for improving password strength.
- Hides password input using Python's `getpass` module.
- Includes automated unit tests.

## Requirements

- Python 3.10 or higher.
- No external packages required.

## Project Structure

```text
Password-Strength-Checker/
│
├── src/
│   └── password_checker.py
│
├── tests/
│   └── test_password_checker.py
│
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd Password-Strength-Checker
```

## Usage

Run the program:

```bash
python src/password_checker.py
```

Enter a test password when prompted.

## Running Tests

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

## Security Notes

- Passwords are entered using `getpass` to prevent them from being displayed in the terminal.
- The program does not store or transmit passwords.
- This project uses a basic educational scoring system.
- A Strong result does not guarantee that a password is secure or has never been exposed in a data breach.
- Do not use real passwords when testing.

## License

This project is licensed under the MIT License.