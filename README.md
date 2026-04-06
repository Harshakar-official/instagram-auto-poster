# Instagram Auto-Poster Bot

A completely **FREE**, fully automated AI system that posts daily on an Instagram Business account. Supports AI-generated images with **zero API costs**.

## Features

- **AI-Generated Content**: Educational cybersecurity captions with hashtags
- **AI Images (FREE)**: Uses Pollinations.ai for image generation - no API key needed!
- **Fallback Images**: Unsplash integration for stock photos
- **Auto-Posting**: GitHub Actions (6x daily) + Local scheduler
- **Missed Post Recovery**: Automatically posts missed content on startup
- **Error Handling**: Retry mechanism with multiple image hosting fallbacks
- **Analytics**: Track engagement via Instagram API

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Harshakar-official/instagram-auto-poster.git
cd instagram-auto-poster

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# Run!
./post.sh ai
```

---

## Security Setup

### GitHub Secrets (Required)

Go to **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Where to Get |
|--------|--------------|
| `ACCESS_TOKEN` | [Graph API Explorer](https://developers.facebook.com/tools/explorer/) |
| `INSTAGRAM_USER_ID` | [Graph API Explorer](https://developers.facebook.com/tools/explorer/) |
| `FACEBOOK_PAGE_ID` | [Graph API Explorer](https://developers.facebook.com/tools/explatcher/) |
| `IMAGE_SOURCE` | `unsplash` or `ai` |
| `UNSPLASH_ACCESS_KEY` | [Unsplash Developers](https://unsplash.com/developers) |
| `NICHE` | `cybersecurity` |
| `USE_AI_IMAGES` | `true` or `false` |

See [SECURITY.md](SECURITY.md) for detailed security guide.

---

## Commands

```bash
# Post with AI-generated image (FREE!)
./post.sh ai

# Post with infographic style
./post.sh post

# Auto-post scheduler (with missed post detection)
./post.sh schedule
./post.sh schedule-ai

# Health check
./post.sh health

# View analytics
./post.sh analytics
```

---

## File Structure

```
instagram-auto-poster/
├── main.py                    # Main bot
├── config.py                  # Configuration
├── ai_image.js               # AI image generation (Pollinations.ai)
├── post.sh                   # Helper commands
├── startup.sh                # Startup with missed post detection
├── modules/
│   ├── content_generator.py  # Caption & hashtag generator
│   ├── image_generator.py   # Image handler
│   └── instagram_poster.py   # Instagram API
├── .github/workflows/
│   └── post.yml             # CI/CD automation
├── SECURITY.md              # Security guide
├── SETUP_GUIDE.md          # Full setup instructions
├── QUICK_REFERENCE.md       # Quick reference card
└── .env.example            # Template (safe to share)
```

---

## Image Options

| Type | Command | Cost | Setup |
|------|---------|------|-------|
| AI Generated | `--ai` | FREE | None needed |
| Unsplash | `--post` | FREE | API key |
| Infographic | `--post` | FREE | Built-in |

---

## Posting Schedule

Default: **7AM, 9AM, 12PM, 3PM, 6PM, 9PM** (6x daily)

Edit `.github/workflows/post.yml` to customize:
```yaml
cron: '0 7,9,12,15,18,21 * * *'
```

---

## Local Startup Service

Install the macOS startup service:
```bash
./install_startup.sh
```

The bot will:
1. Start automatically on Mac boot
2. Check for any missed posts
3. Post missed content immediately
4. Continue with scheduled posting

---

## Security Checklist

- [ ] `.env` is in `.gitignore` (never committed)
- [ ] All secrets in GitHub Secrets (not in code)
- [ ] `.env.example` uses placeholder values
- [ ] `post_state.json` in `.gitignore`
- [ ] Tokens rotated regularly (every 60 days)

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `API access blocked` | Regenerate access token |
| `Permission denied` | Re-authorize in Graph API Explorer |
| `Media upload failed` | Image hosting may be down, retry later |
| `Rate limit exceeded` | Wait 1 hour |

---

## Support

1. Check `instagram_bot.log` for detailed logs
2. Run `./post.sh health` to verify connection
3. Verify secrets in GitHub Settings
4. Check [GitHub Actions](https://github.com/Harshakar-official/instagram-auto-poster/actions)

---

**License**: MIT - Use freely!
