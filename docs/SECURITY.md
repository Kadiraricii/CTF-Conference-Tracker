# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Please report vulnerabilities to **security@example.com** (replace with actual contact). Do not open public issues for sensitive security flaws.

## Secret Key Policy

### 1. Storage
- **NEVER** commit `SECRET_KEY` or other sensitive credentials to the repository.
- Use `.env` files for local development (which are `.gitignore`'d).
- Use environment variables or secrets management (e.g., AWS Secrets Manager, Vault, GitHub Secrets) in production.

### 2. Default Values
- The `SECRET_KEY` in `.env.example` is a meaningless placeholder. **DO NOT USE IT IN PRODUCTION.**

### 3. Rotation
Rotate the `SECRET_KEY` immediately if:
- You suspect a leak.
- A developer with access leaves the team.
- Regularly (e.g., every 6 months) as a best practice.

**Rotation Steps:**
1. Generate a new secure key (e.g., `openssl rand -hex 32`).
2. Update the environment variable in your deployment dashboard / secrets manager.
3. Restart the application.
   - *Note:* This will invalidate existing sessions/tokens signed with the old key.

## Emergency Procedures (Leak Response)

If a secret is committed to git history:

1. **Revoke the Secret:** Immediately invalidate the leaked API key or password.
2. **Rotate:** Generate a new secret and update the application config.
3. **Clean History:**
   - Use [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) or `git-filter-repo` to remove the file/string from history.
   - **Warning:** This rewrites git history and requires a `git push --force`. All collaborators must re-clone the repo.
