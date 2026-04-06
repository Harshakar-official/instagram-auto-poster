# Security Guide

## Overview

This document explains how credentials and secrets are managed securely in this project.

---

## What is PUBLIC (in repository)

These files are safe to share publicly:

```
├── ai_image.js              # AI image generation code
├── main.py                  # Main bot logic
├── config.py                # Configuration (no secrets)
├── post.sh                  # Helper script
├── startup.sh               # Startup script
├── modules/
│   ├── content_generator.py
│   ├── image_generator.py
│   └── instagram_poster.py
├── .github/workflows/
│   └── post.yml            # Uses secrets, not values
├── .env.example            # Template with placeholder values
├── requirements.txt
├── .gitignore
└── README.md
```

---

## What is PRIVATE (never commit)

**ALWAYS kept local, NEVER pushed to GitHub:**

| File | Why Private | Contains |
|------|-------------|----------|
| `.env` | Contains live credentials | Access tokens, API keys |
| `post_state.json` | Contains posting schedule | Post timing data |
| `venv/` | Contains installed packages | System-specific |
| `node_modules/` | Contains npm packages | System-specific |
| `*.log` | Contains runtime info | Timestamps, post IDs |
| `images/*` | Contains generated images | Content |

---

## GitHub Secrets (for CI/CD)

All sensitive configuration is stored as **GitHub Secrets**:

| Secret Name | Purpose | Example |
|-------------|---------|---------|
| `ACCESS_TOKEN` | Meta/Facebook API token | `EAAU...` |
| `INSTAGRAM_USER_ID` | Instagram account ID | `178414...` |
| `FACEBOOK_PAGE_ID` | Facebook Page ID | `123456...` |
| `IMAGE_SOURCE` | Image source type | `unsplash` |
| `UNSPLASH_ACCESS_KEY` | Unsplash API key | `xxx...` |
| `NICHE` | Content niche | `cybersecurity` |
| `USE_AI_IMAGES` | Enable AI images | `false` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### Adding/Updating Secrets

```bash
# Using GitHub CLI
gh secret set ACCESS_TOKEN -b "your-token-here"
gh secret set INSTAGRAM_USER_ID -b "your-id-here"
```

Or via GitHub UI:
1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

---

## Local Setup Security

### 1. Create your `.env` file

```bash
# Copy the example
cp .env.example .env

# Edit with your actual values
nano .env
```

### 2. Never share your `.env` file

```bash
# Verify .env is in .gitignore
cat .gitignore | grep "\.env"
# Should output: .env
```

### 3. Verify no secrets in repo

```bash
# Check for accidental commits
git log --all --full-history -- "*/.env"

# If found, remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

---

## Token Security

### Meta/Facebook Token

1. **Generate**: https://developers.facebook.com/tools/explorer/
2. **Extend**: Click (i) → Extend Access Token
3. **Store**: Add to GitHub Secrets AND local `.env`
4. **Rotate**: Regenerate every 60 days

### Unsplash API Key

1. **Get**: https://unsplash.com/developers
2. **Create App**: Generate Access Key
3. **Store**: GitHub Secrets + local `.env`
4. **Free Tier**: 50 requests/hour

---

## Security Best Practices

### DO ✅
- Store all tokens in GitHub Secrets
- Keep `.env` local only
- Use `gh secret list` to verify secrets exist
- Rotate tokens regularly
- Use `.gitignore` to prevent accidental commits
- Review code before pushing

### DON'T ❌
- Commit `.env` to repository
- Hardcode tokens in code
- Share access tokens in chat/email
- Use short-lived tokens in CI/CD
- Store tokens in public files

---

## Verification Commands

```bash
# Check what will be committed
git status

# Verify .env is ignored
git check-ignore .env

# List GitHub secrets
gh secret list

# Check for secrets in history
git log --all --source --remotes -S "EAAU"
```

---

## If You Accidentally Expose Secrets

1. **Immediately rotate** the exposed token
2. **Remove from history**: `git filter-branch` or BFG Repo-Cleaner
3. **Update GitHub Secrets** with new values
4. **Update local `.env`** files
5. **Enable branch protection** to prevent future issues

```bash
# Install BFG for cleaning history
brew install bfg

# Clean secrets from history
bfg --replace-text banned.txt repo/
git push --force --all
```

---

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Meta API Security](https://developers.facebook.com/docs/apps/security)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**Remember**: Once a secret is public, assume it's compromised and rotate it immediately.
