#!/bin/bash
# run-tracker.sh — Runner script for the AI News Tracker
#
# Usage:
#   ./scripts/run-tracker.sh              # Normal run
#   ./scripts/run-tracker.sh --dry-run    # Check without generating
#   ./scripts/run-tracker.sh --source anthropic  # Single source
#
# Cron example (every 4 hours):
#   0 */4 * * * /Users/ian/egoistai/scripts/run-tracker.sh >> /Users/ian/egoistai/logs/cron.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/tracker-venv"
TRACKER="$SCRIPT_DIR/ai-news-tracker.py"

# Ensure claude CLI is in PATH (common install locations)
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

# Activate the virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --quiet feedparser requests beautifulsoup4
fi

source "$VENV_DIR/bin/activate"

# Run the tracker, passing along any arguments
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running AI News Tracker..."
python "$TRACKER" "$@"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done."
