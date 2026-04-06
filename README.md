# Instagram Auto-Poster Bot

A completely FREE, fully automated AI system that posts daily on an Instagram Business account.

## Features

- **AI-Generated Content**: Uses Hugging Face (Mistral/LLaMA) for caption and hashtag generation
- **Image Generation**: Supports Stable Diffusion API or free Unsplash images
- **Auto-Posting**: Scheduled posting via GitHub Actions (2x daily)
- **Error Handling**: Retry mechanism and logging
- **Analytics**: Track likes, comments, and engagement

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Instagram Setup](#instagram-setup)
3. [Meta Developer Setup](#meta-developer-setup)
4. [GitHub Setup](#github-setup)
5. [Configuration](#configuration)
6. [Local Testing](#local-testing)
7. [Niche Customization](#niche-customization)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

You'll need:
- Free Instagram Business or Creator account
- Free Facebook Page
- Free GitHub account
- Hugging Face account (optional, for AI captions)
- Unsplash account (optional, for free images)

---

## Instagram Setup

### Step 1: Convert to Business Account

1. Open Instagram app
2. Go to **Settings** (gear icon)
3. Tap **Account**
4. Tap **Switch to Professional Account**
5. Choose **Business** or **Creator**
6. Follow the prompts

### Step 2: Connect to Facebook Page

1. Go to **Settings** > **Account**
2. Tap **Page**
3. Tap **Create New Facebook Page** or **Connect Existing Page**
4. Select your Facebook Page
5. Follow the prompts to link

### Step 3: Note Your Instagram User ID

After setup, get your Instagram User ID:
1. Go to [facebook.com/business点位/facebook-pixel](https://business.facebook.com)
2. Navigate to your Instagram account connected to your Page
3. Your Instagram Account ID will be listed

Or use this tool: [Instagram User ID Finder](https://mega.nz/file/j9xGDBZb#m47QZ8YgcoI9tTMlgvJU33vgXgkQ3L_h3mRnRIcRBmI)

---

## Meta Developer Setup

### Step 1: Create Meta App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **My Apps**
3. Click **Create App**
4. Select **Consumer** app type
5. Enter app name (e.g., "Instagram Auto-Poster")
6. Click **Create App**

### Step 2: Add Instagram Graph API

1. In your app dashboard, click **Add Products**
2. Find **Instagram Graph API**
3. Click **Set Up**
4. Select your app and continue

### Step 3: Configure Instagram Product

1. Go to **Instagram Graph API** in sidebar
2. Click **API Setup**
3. Add your Instagram Business account:
   - Click **Add Instagram Accounts**
   - Enter your Instagram username
   - Authorize the connection

### Step 4: Generate Access Token

1. Go to **Tools** > **Graph API Explorer**
2. Select your app from dropdown
3. Click **Generate Access Token**
4. Grant permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
   - `instagram_manage_insights`

5. Copy the generated token

### Step 5: Get Instagram Account ID

Use the Graph API Explorer:
1. Select `instagram_basic` permission
2. Query: `GET /me/accounts`
3. Get your Page ID
4. Query: `GET /{page-id}?fields=instagram_business_account`
5. Get your Instagram Account ID

---

## Hugging Face Setup (Optional - For AI Captions)

### Step 1: Create Account

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up for free

### Step 2: Get API Token

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **New Token**
3. Name it "Instagram Bot"
4. Select **Read** type
5. Copy the token

---

## Unsplash Setup (For Free Images)

### Step 1: Create Account

1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Click **Register as a developer**
3. Create a new application

### Step 2: Get Access Key

1. After app registration, you'll receive:
   - Access Key
   - Secret Key
2. Use the **Access Key**

Note: Free tier = 50 requests/hour

---

## GitHub Setup

### Step 1: Create Repository

1. Go to [github.com](https://github.com)
2. Click **New repository**
3. Name it "instagram-auto-poster"
4. Make it **Private** (recommended)
5. Click **Create repository**

### Step 2: Upload Files

1. Click **uploading an existing file**
2. Upload all files from this project:
   - `main.py`
   - `config.py`
   - `requirements.txt`
   - `modules/content_generator.py`
   - `modules/image_generator.py`
   - `modules/instagram_poster.py`
   - `.github/workflows/post.yml`

### Step 3: Add Secrets

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `INSTAGRAM_USER_ID` | Your Instagram Account ID |
| `ACCESS_TOKEN` | Your Meta Access Token |
| `FACEBOOK_PAGE_ID` | Your Facebook Page ID |
| `HUGGINGFACE_TOKEN` | Your Hugging Face API token (optional) |
| `UNSPLASH_ACCESS_KEY` | Your Unsplash Access Key |
| `IMAGE_SOURCE` | `unsplash` or `stable_diffusion` |
| `NICHE` | Your niche (e.g., `food`, `travel`) |

### Step 4: Configure Schedule (Optional)

Edit `.github/workflows/post.yml`:

```yaml
schedule:
  - cron: '0 9,18 * * *'  # 9 AM and 6 PM daily
```

Schedule examples:
- **Every 6 hours**: `cron: '0 */6 * * *'`
- **Once daily**: `cron: '0 9 * * *'`
- **Twice daily**: `cron: '0 9,18 * * *'`
- **Every Monday**: `cron: '0 9 * * 1'`

---

## Configuration

Edit `config.py` or use environment variables:

```python
# Your niche (required)
NICHE = "food"  # Options: food, travel, fitness, fashion, tech, lifestyle, nature, business, art, photography

# Image source
IMAGE_SOURCE = "unsplash"  # Options: unsplash, stable_diffusion

# Posting schedule
POSTING_TIMES = "09:00,18:00"

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 60
```

---

## Local Testing

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create .env File

Create a `.env` file:

```env
INSTAGRAM_USER_ID=your_instagram_id
ACCESS_TOKEN=your_access_token
FACEBOOK_PAGE_ID=your_page_id
HUGGINGFACE_TOKEN=your_huggingface_token
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your_unsplash_key
NICHE=food
LOG_LEVEL=INFO
```

### 3. Run Locally

```bash
python main.py
```

### Test Commands

```bash
# Health check
python main.py --health

# Get analytics
python main.py --analytics
```

---

## Niche Customization

Supported niches:
- `food` - Food photography and recipes
- `travel` - Travel and adventure
- `fitness` - Gym and health
- `fashion` - Style and outfits
- `tech` - Technology
- `lifestyle` - General lifestyle
- `nature` - Nature and wildlife
- `business` - Business and entrepreneurship
- `art` - Art and creativity
- `photography` - Photo tips and inspiration

### Adding Custom Niches

Edit `modules/content_generator.py`:

```python
# Add to prompts dict:
"custom_niche": "Generate an engaging caption about...",
"custom_niche": "Professional custom_niche photography..."
```

---

## Image Generation Options

### Option A: Unsplash (Recommended - Free)

Uses high-quality free stock photos:
```env
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your_key
```

### Option B: Stable Diffusion API

Use Replicate or other Stable Diffusion APIs:
```env
IMAGE_SOURCE=stable_diffusion
STABLE_DIFFUSION_API_URL=https://api.replicate.com/v1/predictions
STABLE_DIFFUSION_API_KEY=your_key
```

### Option C: Local Stable Diffusion

Run Stable Diffusion locally with [ComfyUI](https://github.com/comfyanonymous/ComfyUI) or [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

---

## Troubleshooting

### Common Errors

**"Page not found or not accessible"**
- Verify Facebook Page is linked to Instagram
- Regenerate access token

**"Permission denied"**
- Re-authorize with required permissions
- Check token hasn't expired

**"Media upload failed"**
- Image may be too large (max 8MB)
- Check image format (JPG/PNG)

**"Rate limit exceeded"**
- Wait 1 hour
- Reduce posting frequency

### Debug Mode

Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

Check logs:
```bash
tail -f instagram_bot.log
```

---

## API Rate Limits

| API | Limit |
|-----|-------|
| Instagram Graph API | 200 requests/hour |
| Unsplash | 50 requests/hour |
| Hugging Face | Varies by model |

---

## Security Best Practices

1. **Never commit .env files**
2. **Use GitHub Secrets** for all credentials
3. **Rotate tokens** monthly
4. **Use private repositories** for sensitive projects

---

## File Structure

```
instagram-auto-poster/
├── main.py                          # Main bot script
├── config.py                        # Configuration
├── requirements.txt                 # Dependencies
├── modules/
│   ├── content_generator.py        # AI caption/hashtag generator
│   ├── image_generator.py          # Image fetcher/generator
│   └── instagram_poster.py         # Instagram API integration
├── images/                          # Downloaded/generated images
├── .github/
│   └── workflows/
│       └── post.yml                # GitHub Actions workflow
└── README.md                        # This file
```

---

## Support

For issues:
1. Check [instagram_bot.log](instagram_bot.log)
2. Verify all secrets are set correctly
3. Ensure Meta token is valid
4. Check GitHub Actions logs

---

## License

MIT License - Use freely for personal and commercial projects.

---

## Contributing

Contributions welcome! Please submit PRs with tests and documentation.

---

**Good luck with your Instagram automation! 🚀**
