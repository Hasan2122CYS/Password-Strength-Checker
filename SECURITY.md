# Security Policy

## Scope

This project is a local password guessability checker with an optional
third-party compromised-password lookup. It is not an authentication service
or password manager.

## Reporting a vulnerability

Please do not publish passwords, tokens, private keys, or other secrets in an
issue. Report security concerns through a private channel provided by the
repository maintainer.

## Handling rules

- Never commit real passwords or test fixtures containing personal secrets.
- Do not add password logging, analytics, telemetry, or persistence without
  explicit design review and user consent.
- Keep the online breach lookup opt-in.
- Do not send the password or complete password hash to the HIBP range API.
