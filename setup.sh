#!/bin/bash

# VAPTANIX Instagram Auto-Poster Setup Script

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           VAPTANIX Instagram Auto-Poster Setup          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Please create a .env file with your credentials:"
    echo ""
    cat << 'EOF'
# Create .env file with:
INSTAGRAM_USER_ID=your_instagram_id
ACCESS_TOKEN=your_facebook_access_token
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=your_unsplash_key
NICHE=cybersecurity

# Example .env:
INSTAGRAM_USER_ID=17841442095397155
ACCESS_TOKEN=EAAU783h2Nuo...
IMAGE_SOURCE=unsplash
UNSPLASH_ACCESS_KEY=31MlKOmjqDjDIaaar8bAkMv3CnWR...
NICHE=cybersecurity
EOF
    echo ""
    echo "Create your .env file and run: ./post.sh post"
else
    echo "✅ .env file found"
    echo ""
    echo "🚀 Ready to post!"
    echo ""
    echo "Commands:"
    echo "  ./post.sh post       - Post now"
    echo "  ./post.sh health     - Check connection"
    echo "  ./post.sh analytics  - View stats"
    echo "  ./post.sh schedule   - Auto-post daily"
fi
