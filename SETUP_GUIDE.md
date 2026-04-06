# Complete Setup Guide - Instagram Auto-Poster

This guide provides detailed step-by-step instructions to set up your free Instagram automation system.

---

## PHASE 1: INSTAGRAM SETUP

### Step 1.1: Convert to Business Account

**On Mobile (Instagram App):**
1. Open Instagram and go to your profile
2. Tap the **hamburger menu (☰)** in top right
3. Tap **Settings and privacy**
4. Tap **Account tools and controls**
5. Tap **Add new professional account**
6. Select **Business** (or Creator)
7. Tap **Continue**
8. Choose category (e.g., Food, Travel, etc.)
9. Tap **Done**
10. Your account is now a Business account

**On Desktop (Browser):**
1. Go to [instagram.com](https://instagram.com)
2. Click your profile picture > Settings (⚙️)
3. Click **Account**
4. Click **Switch to professional account**
5. Follow the prompts

---

### Step 1.2: Connect to Facebook Page

**Method A - Through Instagram App:**
1. Go to your Instagram profile
2. Tap **Edit profile**
3. Under "Public business information", tap **Page**
4. Tap **Create Facebook Page** OR **Connect existing Page**
5. If creating new:
   - Enter Page name
   - Select category
   - Click **Create Page**
6. If connecting existing:
   - Select your Facebook Page
   - Tap **Connect**

**Method B - Through Facebook:**
1. Go to [facebook.com](https://facebook.com)
2. Click **Create** > **Page**
3. Select page type (Local Business or Company)
4. Enter name and category
5. Click **Create Page**
6. Go to **Settings** > **Instagram**
7. Click **Connect account**
8. Enter your Instagram credentials

---

### Step 1.3: Get Your Instagram Account ID

**Option A - Use Meta Business Suite:**
1. Go to [business.facebook.com](https://business.facebook.com)
2. Click **All tools** in sidebar
3. Click **Instagram** (under Channels)
4. You'll see your connected Instagram accounts
5. Your Account ID is shown there (numeric, like 17841401234567890)

**Option B - Use Graph API Explorer:**
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **My Apps** > **Graph API Explorer** (in Tools menu)
3. Select your app from dropdown
4. Click **Generate Access Token** (you'll do this in Phase 2)
5. In the query box, enter: `me?fields=accounts{instagram_business_account}`
6. Click **Submit**
7. Your Instagram Account ID will be in the response

**Option C - Third-party tool:**
1. Visit: [meeum.com](https://meeum.com) (free)
2. Enter your Instagram username
3. Get your numeric Account ID

---

## PHASE 2: META DEVELOPER SETUP

### Step 2.1: Create Meta Developer Account

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **Log In** (top right)
3. Log in with your Facebook account (same one linked to your Page)
4. First time? Click **Get Started** and accept terms

---

### Step 2.2: Create a New App

1. Click **My Apps** (top right)
2. Click **Create App**
3. Select app type: **Consumer** (NOT Business)
4. Click **Next**
5. Enter App Display Name: `Instagram Auto-Poster` (or any name)
6. Enter App Contact Email: your email
7. Click **Create App**
8. Complete security check (enter captcha if shown)
9. You'll land on your app dashboard

---

### Step 2.3: Add Instagram Graph API Product

1. In your app dashboard, look for **Add Products to Your App**
2. Find **Instagram Graph API** card
3. Click **Set Up**
4. Click **Create App** if prompted
5. Select your app again
6. Click **Configure** (API Setup section)
7. Click **Add Instagram Accounts**
8. Enter your Instagram username
9. Click **Authorize** and log in to your Instagram account
10. Your Instagram account should now show as connected

---

### Step 2.4: Generate Access Token

**IMPORTANT: Do these steps in order:**

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **Tools** (top menu) > **Graph API Explorer**
3. Select your app from dropdown (top left)
4. Click **Generate Access Token**

**A popup will appear - DO THIS:**
5. Check these permissions:
   - ✅ `instagram_basic`
   - ✅ `instagram_content_publish`
   - ✅ `pages_read_engagement`
   - ✅ `instagram_manage_insights`
6. Click **Generate Token**
7. Facebook will ask you to authorize - click **Continue as [Your Name]**
8. Click **OK** to confirm permissions
9. Your **Access Token** will appear in the text box
10. **COPY THIS TOKEN IMMEDIATELY** (long alphanumeric string)

**⚠️ IMPORTANT: Long-term tokens require Exchange:**
11. Click the **i** icon next to your token
12. Click **Open in Access Token Debugger**
13. Scroll down and click **Extend Access Token**
14. Copy the new extended token

---

### Step 2.5: Get Your Page ID and Instagram Account ID

**Back in Graph API Explorer:**

1. Make sure your app is selected
2. Make sure your extended Access Token is entered
3. In the query field, enter: `me/accounts`
4. Click **Submit**
5. You'll see JSON response with:
   ```
   {
     "data": [
       {
         "name": "Your Page Name",
         "id": "123456789012345"  <-- THIS IS YOUR PAGE ID
       }
     ]
   }
   ```
6. Copy your Page ID

**Now get Instagram Account ID:**
7. Clear the query field
8. Enter: `{your-page-id}?fields=instagram_business_account`
   (Replace with your actual Page ID)
9. Click **Submit**
10. You'll see:
    ```
    {
      "instagram_business_account": {
        "id": "17841401234567890"  <-- THIS IS YOUR INSTAGRAM USER ID
      }
    }
    ```
11. Copy this Instagram Account ID

**Save these 2 values:**
- ✅ `ACCESS_TOKEN` = Your extended access token
- ✅ `INSTAGRAM_USER_ID` = The instagram_business_account id (e.g., 17841401234567890)
- ✅ `FACEBOOK_PAGE_ID` = Your Page ID

---

## PHASE 3: HUGGING FACE SETUP (Optional)

This enables AI-powered caption generation.

### Step 3.1: Create Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click **Sign Up**
3. Enter email, create password, or use Google/GitHub login
4. Verify email if required
5. You're now on the dashboard

### Step 3.2: Get API Token

1. Click your profile picture (top right)
2. Click **Settings**
3. Click **Access Tokens** (in sidebar)
4. Click **New Token**
5. Enter Token name: `Instagram-Bot`
6. Select Type: **Read**
7. Click **Generate token**
8. Click the **copy icon** next to your new token
9. Save this token (starts with `hf_`)

**Your token is:** `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## PHASE 4: UNSPLASH SETUP (Optional)

This enables free high-quality images.

### Step 4.1: Register as Developer

1. Go to [unsplash.com/developers](https://unsplash.com/developers)
2. Click **Register as a developer**
3. Enter your details:
   - Project name: `Instagram Auto-Poster`
   - Description: `Automated Instagram posting with free stock images`
4. Accept Terms of Use
5. Click **Submit application**

### Step 4.2: Create New Application

1. Go to [unsplash.com/developers/applications](https://unsplash.com/developers/applications)
2. Click **New Application**
3. Accept the API guidelines
4. Fill in:
   - App name: `Instagram-Bot`
   - Description: `Free stock images for automated Instagram posts`
5. Click **Create application**

### Step 4.3: Get Your Access Key

1. On your app page, find **Keys**
2. Copy the **Access Key** (not the Secret Key)
3. Your Access Key looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## PHASE 4B: AI IMAGE GENERATION (COMPLETELY FREE!)

**No setup required!** The system uses Pollinations.ai for AI-generated images at no cost.

### How to Use AI Images

```bash
# Post with AI-generated image
./post.sh ai

# Or with Python directly
source venv/bin/activate
python main.py --ai

# Schedule with AI images
./post.sh schedule-ai
```

### Enable by Default

Add to your `.env` file:
```
USE_AI_IMAGES=true
```

### Models Available

| Model | Speed | Quality |
|-------|-------|---------|
| flux | Slower | Higher quality |
| turbo | Faster | Good quality |

---

## PHASE 5: GITHUB SETUP

---

## PHASE 5: GITHUB SETUP

### Step 5.1: Create GitHub Account (if not done)

1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Enter email, password, username
4. Verify your account
5. You're ready!

### Step 5.2: Create Repository

1. Click **+** (top right) > **New repository**
2. Fill in:
   - Repository name: `instagram-auto-poster`
   - Description: `Free AI-powered Instagram auto-poster`
   - Select **Private** (recommended)
   - ✅ Add a README file
3. Click **Create repository**

### Step 5.3: Upload Your Files

**Option A - Upload Files:**
1. In your new repo, click **uploading an existing file**
2. Drag and drop all these files:
   ```
   main.py
   config.py
   requirements.txt
   .env.example
   .gitignore
   README.md
   ai_image.js              # NEW! AI image generation
   post.sh                   # Helper script
   modules/content_generator.py
   modules/image_generator.py
   modules/instagram_poster.py
   .github/workflows/post.yml
   images/.gitkeep
   ```
3. Click **Commit changes**

**Option B - Upload Folder by Folder:**
1. Create each folder manually
2. Click **Add file** > **Create new file**
3. Name it and paste content
4. Click **Commit changes**

---

### Step 5.4: Add Secrets

1. In your repo, click **Settings** (tab at top)
2. Click **Secrets and variables** (sidebar) > **Actions**
3. Click **New repository secret**

**Add each secret (click New secret for each):**

| Secret Name | Value | Where to get it |
|------------|-------|----------------|
| `INSTAGRAM_USER_ID` | `17841401234567890` | Phase 2.5 |
| `ACCESS_TOKEN` | `your-extended-token` | Phase 2.4 |
| `FACEBOOK_PAGE_ID` | `123456789012345` | Phase 2.5 |
| `HUGGINGFACE_TOKEN` | `hf_xxxxxxxx` | Phase 3.2 (optional) |
| `UNSPLASH_ACCESS_KEY` | `xxxxxxxxxxxxxxxx` | Phase 4.3 (optional) |
| `IMAGE_SOURCE` | `unsplash` | Use `unsplash` or `stable_diffusion` |
| `NICHE` | `food` | Your niche: food, travel, fitness, etc. |

**For IMAGE_SOURCE:**
- If using Unsplash: `unsplash`
- If using Stable Diffusion: `stable_diffusion`

**For NICHE, choose one:**
- `food` - Food photography
- `travel` - Travel/adventure
- `fitness` - Gym/health
- `fashion` - Style
- `tech` - Technology
- `lifestyle` - General
- `nature` - Nature
- `business` - Business
- `art` - Art/creative
- `photography` - Photography

---

### Step 5.5: Enable GitHub Actions

1. In your repo, click **Actions** tab (top menu)
2. If you see "Workflows disabled", click **I understand my workflows, go ahead and enable them**
3. You should see the `Instagram Auto-Poster` workflow
4. It will run automatically at scheduled times

### Step 5.6: Trigger First Run (Manual Test)

1. Click **Actions** tab
2. Click on **Instagram Auto-Poster**
3. Click **Run workflow** (right side)
4. Click **Run workflow** again (green button)
5. Wait for it to complete
6. Click on the run to see logs

---

## PHASE 6: LOCAL SETUP (Optional - for testing)

### Step 6.1: Install Python

1. Download Python: [python.org/downloads](https://python.org/downloads)
2. Download Python 3.11 or 3.12
3. Run installer, **CHECK "Add Python to PATH"**
4. Click Install Now
5. Verify: Open Terminal, type `python --version`

### Step 6.2: Install Dependencies

```bash
# Open Terminal/Command Prompt
cd path/to/instagram-auto-poster

# Install requirements
pip install -r requirements.txt
```

### Step 6.3: Create .env File

Create a file named `.env` (with the dot):
```env
INSTAGRAM_USER_ID=17841401234567890
ACCESS_TOKEN=your-extended-access-token
FACEBOOK_PAGE_ID=123456789012345
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxx
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
NICHE=food
LOG_LEVEL=INFO
```

### Step 6.4: Test Locally

```bash
# Run the bot
python main.py

# Check health
python main.py --health

# Get analytics
python main.py --analytics
```

---

## VERIFICATION CHECKLIST

Before going live, verify everything:

- [ ] Instagram account is Business/Professional type
- [ ] Facebook Page is created and linked
- [ ] Meta App is created with Instagram Graph API
- [ ] Access Token has required permissions
- [ ] Instagram Account ID is obtained
- [ ] GitHub repo is created
- [ ] All secrets are added to GitHub
- [ ] GitHub Actions is enabled
- [ ] First test run completed successfully

---

## POSTING SCHEDULE

The default schedule posts at **9:00 AM and 6:00 PM daily** (UTC time).

To change, edit `.github/workflows/post.yml`:

```yaml
schedule:
  - cron: '0 9,18 * * *'
```

**Schedule Examples:**
- Every day at 9 AM only: `cron: '0 9 * * *'`
- Every 6 hours: `cron: '0 */6 * * *'`
- Once per week (Monday): `cron: '0 9 * * 1'`
- 3 times daily: `cron: '0 6,12,18 * * *'`

**Note:** Times are in UTC. Adjust for your timezone:
- EST (UTC-5): Subtract 5 from your hour
- PST (UTC-8): Subtract 8 from your hour

---

## TROUBLESHOOTING

### "Page not found or not accessible"
- Re-link Instagram to Facebook Page
- Regenerate access token in Graph API Explorer
- Check token hasn't expired

### "Permission denied"
- Re-authorize in Graph API Explorer
- Make sure you checked all 4 permissions
- Extend your access token

### "Media upload failed"
- Image may exceed 8MB limit
- Check image format (use JPG or PNG)
- Ensure Instagram account is Business type

### "Rate limit exceeded"
- Wait 1 hour
- Reduce posting frequency in workflow

### "Token has expired"
- Go to Graph API Explorer
- Click **Extend Access Token**
- Update the secret in GitHub

### Bot not posting
- Check GitHub Actions > All workflows
- Click on failed run for error details
- Check instagram_bot.log file

---

## SUPPORT

For help:
1. Check GitHub Actions logs for errors
2. Run `python main.py --health` locally
3. Verify all secrets are correct
4. Ensure Meta token is valid

---

**Setup complete! Your bot will now post automatically. 🚀**
