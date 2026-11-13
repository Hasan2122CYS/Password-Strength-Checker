import unittest

from src.password_checker import check_password_strength


class TestPasswordStrengthChecker(unittest.TestCase):

    def test_weak_password(self):
        strength, feedback = check_password_strength("abc")

        self.assertEqual(strength, "Weak")
        self.assertTrue(len(feedback) > 0)

    def test_medium_password(self):
        strength, feedback = check_password_strength("Abcdef12")

        self.assertEqual(strength, "Medium")

    def test_strong_password(self):
        strength, feedback = check_password_strength("Abcdef12!xyz")

        self.assertEqual(strength, "Strong")
        self.assertEqual(feedback, [])


if __name__ == "__main__":
    unittest.main()