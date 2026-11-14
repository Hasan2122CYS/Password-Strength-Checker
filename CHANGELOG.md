# Changelog

## 1.0.0

- Replaced hand-written password rules with the zxcvbn guessability estimator.
- Separated analysis, CLI, and optional breach lookup into distinct modules.
- Added an opt-in Have I Been Pwned Pwned Passwords range lookup using
  k-anonymity and response padding.
- Added a 72-character analysis limit to bound estimator work.
- Added unit tests and project packaging metadata.
