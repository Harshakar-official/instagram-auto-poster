# Quick Reference Card

## What You Need to Set Up (15 min total)

### Day 1: Meta Developer Setup (~10 min)

1. **developers.facebook.com** → Create App (Consumer type)
2. Add **Instagram Graph API** product
3. **Tools** → **Graph API Explorer**
4. Generate Access Token with these permissions:
   - instagram_basic
   - instagram_content_publish
   - pages_read_engagement
   - instagram_manage_insights
5. Query: `me/accounts` → Get **PAGE_ID**
6. Query: `{PAGE_ID}?fields=instagram_business_account` → Get **INSTAGRAM_USER_ID**

### Day 2: GitHub Setup (~5 min)

1. **github.com** → Create new repo
2. Upload all project files
3. **Settings** → **Secrets** → Add:
   - INSTAGRAM_USER_ID
   - ACCESS_TOKEN
   - FACEBOOK_PAGE_ID
4. Go to **Actions** tab → Enable
5. Click **Run workflow** to test

### Optional (2 min each)

**Unsplash** (free images):
- unsplash.com/developers → Register → Create App
- Add: UNSPLASH_ACCESS_KEY, IMAGE_SOURCE=unsplash

**AI Images (COMPLETELY FREE!)**:
- No setup needed! Uses Pollinations.ai
- Works out of the box
- Use `--ai` flag or set `USE_AI_IMAGES=true`

---

## Secrets to Add in GitHub

| Secret | Where to Get | Required |
|--------|--------------|----------|
| INSTAGRAM_USER_ID | Graph API Explorer (Step 6) | ✅ Yes |
| ACCESS_TOKEN | Graph API Explorer (Step 4) | ✅ Yes |
| FACEBOOK_PAGE_ID | Graph API Explorer (Step 5) | ✅ Yes |
| UNSPLASH_ACCESS_KEY | unsplash.com/developers | ❌ No |
| IMAGE_SOURCE | `unsplash` | ✅ Yes |
| NICHE | `cybersecurity` | ✅ Yes |
| USE_AI_IMAGES | `true` or `false` | ❌ No |

---

## Running Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Post with infographic style
python main.py --post

# Post with FREE AI-generated image (NEW!)
python main.py --ai

# Auto-post daily with AI images
./post.sh schedule-ai

# Other commands
python main.py --health      # Check API connection
python main.py --analytics   # View recent post stats
```

---

## Schedule (edit post.yml)

```yaml
cron: '0 7,9,12,15,18,21 * * *'  # 6 posts daily (UTC)
```

Time zones:
- UTC → Local (subtract hours)
- EST: -5 | PST: -8 | GMT: +0 | CET: +1 | IST: +5.5

---

## File Structure

```
instagram-auto-poster/
├── main.py                      # Run this
├── config.py                    # Settings
├── ai_image.js                  # AI image generation (Pollinations.ai)
├── modules/
│   ├── content_generator.py    # AI captions
│   ├── image_generator.py      # Image fetching
│   └── instagram_poster.py     # API posting
├── .github/workflows/post.yml   # Auto-scheduler
└── images/                      # Temp image storage
```

---

## Common Issues

| Error | Solution |
|-------|----------|
| Token expired | Re-extend in Graph API Explorer |
| Permission denied | Regenerate token with all 4 permissions |
| Media upload failed | Image must be JPG/PNG, max 8MB |
| Rate limit | Wait 1 hour, reduce frequency |
| No posts appearing | Check GitHub Actions → run logs |

---

## Image Options

| Type | Command | Cost |
|------|---------|------|
| Infographic | `--post` | Free |
| AI Generated | `--ai` | FREE (Pollinations.ai) |
| Unsplash | `--post` (with key) | Free |

---

## Flow Diagram

```
GitHub Actions (scheduled)
        ↓
main.py runs
        ↓
┌───────┴───────┐
↓               ↓
AI Captions   Generate Image
              ↓
        ┌─────┴─────┐
        ↓           ↓
   Infographic  AI Images
   (PIL)       (Pollinations.ai)
        ↓           ↓
        └─────┬─────┘
              ↓
        Instagram Graph API
              ↓
        Post Published! ✅
```

---

**Keep this card handy during setup!**
