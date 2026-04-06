#!/bin/bash

# VAPTANIX Instagram Auto-Poster
# Startup script - checks for missed posts and starts scheduler

cd "$(dirname "$0")"
SCRIPT_DIR="$(pwd)"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           VAPTANIX Instagram Auto-Poster                   ║"
echo "║           Startup Check & Scheduler                        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

source venv/bin/activate

echo "[1/3] Checking for missed posts..."
MISSED=$(cd "$SCRIPT_DIR" && python -c "
from post_state import PostState
state = PostState()
missed = state.get_missed_posts()
if missed:
    print(','.join(map(str, missed)))
else:
    print('')
")

if [ -n "$MISSED" ]; then
    echo "⚠️  Found missed posts at hours: $MISSED"
    echo "📤 Posting now..."
    
    for hour in $(echo "$MISSED" | tr ',' ' '); do
        echo "   Posting for scheduled time ${hour}:00..."
        cd "$SCRIPT_DIR" && python main.py --ai --post
        sleep 30
    done
else
    echo "✅ No missed posts"
fi

echo ""
echo "[2/3] Checking last post time..."
cd "$SCRIPT_DIR" && python post_state.py

echo ""
echo "[3/3] Starting scheduler..."
echo "⏰ Posts will run automatically at 7AM, 9AM, 12PM, 3PM, 6PM, 9PM daily"
echo "Press Ctrl+C to stop"
echo ""

cd "$SCRIPT_DIR"
python main.py --schedule --ai
