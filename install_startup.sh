#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     VAPTANIX INSTAGRAM AUTO-POSTER                       ║"
echo "║     Startup Installation Script                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_PATH="$SCRIPT_DIR/com.vaptanix.instagram-poster.plist"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"

echo "📁 Script directory: $SCRIPT_DIR"
echo ""

# Check if running from correct directory
if [ ! -f "$SCRIPT_DIR/main.py" ]; then
    echo "❌ Error: main.py not found!"
    echo "   Please run this script from the Instagram Automation folder"
    exit 1
fi

echo "✅ All files found"

# Create virtual environment if needed
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo "✅ Dependencies installed"

# Create LaunchAgents directory
echo ""
echo "📁 Creating LaunchAgents directory..."
mkdir -p "$LAUNCH_AGENTS"

# Update plist with correct paths
echo "⚙️  Configuring startup service..."
sed -i '' "s|/Users/harshakar/Documents/Instagram%20Automation|$SCRIPT_DIR|g" "$PLIST_PATH"
sed -i '' "s|/Users/harshakar/Documents/Instagram%20Automation|$SCRIPT_DIR|g" "$PLIST_PATH"

# Copy plist to LaunchAgents
cp "$PLIST_PATH" "$LAUNCH_AGENTS/"

# Load the service
echo ""
echo "🚀 Starting the bot service..."
launchctl unload "$LAUNCH_AGENTS/com.vaptanix.instagram-poster.plist" 2>/dev/null
launchctl load "$LAUNCH_AGENTS/com.vaptanix.instagram-poster.plist"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                   ✅ SETUP COMPLETE!                       ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Vaptanix Instagram Auto-Poster is now running!"
    echo ""
    echo "📋 What will happen:"
    echo "   • Bot starts automatically when Mac turns on"
    echo "   • Posts automatically at 9:00 AM daily"
    echo "   • Posts automatically at 6:00 PM daily"
    echo "   • Runs in background (no terminal needed)"
    echo ""
    echo "📊 Commands:"
    echo "   • View logs: tail -f $SCRIPT_DIR/bot.log"
    echo "   • Stop bot: launchctl unload $LAUNCH_AGENTS/com.vaptanix.instagram-poster.plist"
    echo "   • Start bot: launchctl load $LAUNCH_AGENTS/com.vaptanix.instagram-poster.plist"
    echo "   • Restart: launchctl kickstart -k $LAUNCH_AGENTS/com.vaptanix.instagram-poster.plist"
    echo ""
    echo "🌐 Check your Instagram: @vaptanixsecurity"
    echo ""
else
    echo "❌ Failed to start service"
    echo "   Try manually: launchctl load $LAUNCH_AGENTS/com.vaptanix.instagram-poster.plist"
fi
