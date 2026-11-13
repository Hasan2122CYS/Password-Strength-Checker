import getpass
import string


def check_password_strength(password):
    """
    Evaluate password strength using basic security criteria.
    """

    score = 0
    feedback = []

    # Check password length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if len(password) >= 12:
        score += 1

    # Check for lowercase letters
    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # Check for uppercase letters
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # Check for digits
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add numbers.")

    # Check for special characters
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # Determine password strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, feedback


def main():
    print("================================")
    print("     Password Strength Checker")
    print("================================")

    password = getpass.getpass("Enter a password to check: ")

    strength, feedback = check_password_strength(password)

    print(f"\nPassword Strength: {strength}")

    if feedback:
        print("\nSuggestions:")
        for suggestion in feedback:
            print(f"- {suggestion}")
    else:
        print("\nYour password meets all basic criteria.")

    print("\nNote: This is a basic educational checker,")
    print("not a guarantee of password security.")

if __name__ == "__main__":
    main()