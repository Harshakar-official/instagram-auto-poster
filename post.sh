#!/bin/bash

# VAPTANIX Instagram Auto-Poster
# Easy commands to run the bot

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           VAPTANIX Instagram Auto-Poster                   ║"
echo "║           FREE AI Image Generation Ready!                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

source venv/bin/activate

case "$1" in
    "post")
        echo "📤 Creating and posting now (infographic style)..."
        python main.py --post
        ;;
    "ai")
        echo "🤖 Creating and posting with AI-generated image..."
        echo "Using Pollinations.ai - completely FREE!"
        python main.py --ai
        ;;
    "health")
        echo "🔍 Running health check..."
        python main.py --health
        ;;
    "analytics")
        echo "📊 Fetching analytics..."
        python main.py --analytics
        ;;
    "schedule")
        echo "⏰ Starting scheduled mode..."
        echo "Posts will run automatically at 7AM, 9AM, 12PM, 3PM, 6PM, 9PM daily"
        echo "Press Ctrl+C to stop"
        echo ""
        python main.py --schedule
        ;;
    "schedule-ai")
        echo "⏰ Starting scheduled mode with AI images..."
        echo "Using Pollinations.ai for free AI-generated images!"
        echo "Posts at 7AM, 9AM, 12PM, 3PM, 6PM, 9PM daily"
        echo "Press Ctrl+C to stop"
        echo ""
        python main.py --schedule --ai
        ;;
    *)
        echo "Usage: ./post.sh [command]"
        echo ""
        echo "Commands:"
        echo "  ./post.sh post        - Post now (infographic style)"
        echo "  ./post.sh ai          - Post with AI-generated image (FREE!)"
        echo "  ./post.sh health      - Check connection"
        echo "  ./post.sh analytics   - View post stats"
        echo "  ./post.sh schedule    - Auto-post daily (6x/day)"
        echo "  ./post.sh schedule-ai - Auto-post with AI images (FREE!)"
        echo ""
        echo "Or just run: source venv/bin/activate && python main.py"
        ;;
esac
