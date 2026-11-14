import unittest

from password_strength_checker.analyzer import (
    MAX_PASSWORD_LENGTH,
    STRENGTH_LEVELS,
    analyze_password,
)


class TestPasswordAnalyzer(unittest.TestCase):
    def test_empty_password(self):
        result = analyze_password("")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["strength"], "Very Weak")
        self.assertIn("Password cannot be empty.", result["feedback"])

    def test_common_password_is_very_weak(self):
        result = analyze_password("password")
        self.assertEqual(result["score"], 0)
        self.assertEqual(result["strength"], "Very Weak")

    def test_long_passphrase_scores_high_with_pinned_estimator(self):
        result = analyze_password("correct-horse-battery-staple")
        self.assertEqual(result["score"], 4)
        self.assertEqual(result["strength"], "Very Strong")

    def test_result_structure(self):
        result = analyze_password("mango2026")
        self.assertEqual(
            set(result),
            {"score", "strength", "feedback", "guesses"},
        )

    def test_score_and_label_are_consistent(self):
        result = analyze_password("mango2026")
        self.assertIn(result["score"], range(5))
        self.assertEqual(
            result["strength"],
            STRENGTH_LEVELS[result["score"]],
        )

    def test_feedback_is_a_list(self):
        self.assertIsInstance(analyze_password("mango2026")["feedback"], list)

    def test_rejects_non_string_inputs(self):
        for invalid in (None, 123, 12.5, True, [], {}):
            with self.subTest(value=invalid):
                with self.assertRaises(TypeError):
                    analyze_password(invalid)

    def test_accepts_exact_maximum_length(self):
        # Mock zxcvbn so this boundary test is deterministic and inexpensive.
        from unittest.mock import patch

        fake_result = {
            "score": 2,
            "feedback": {"suggestions": []},
            "guesses": 1000,
        }
        with patch(
            "password_strength_checker.analyzer.zxcvbn",
            return_value=fake_result,
        ) as estimator:
            result = analyze_password("a" * MAX_PASSWORD_LENGTH)
        self.assertEqual(result["score"], 2)
        estimator.assert_called_once_with(
            "a" * MAX_PASSWORD_LENGTH,
            max_length=MAX_PASSWORD_LENGTH,
        )

    def test_rejects_password_over_maximum_length(self):
        with self.assertRaises(ValueError):
            analyze_password("a" * (MAX_PASSWORD_LENGTH + 1))

    def test_accepts_unicode(self):
        result = analyze_password("مفتاح-تجريبي-طويل-2026")
        self.assertIn(result["score"], range(5))


if __name__ == "__main__":
    unittest.main()
