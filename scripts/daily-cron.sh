#!/usr/bin/env bash
set -euo pipefail

# EgoistAI Daily Content Pipeline
# Generates articles, validates, builds, commits, and pushes
#
# Usage: bash scripts/daily-cron.sh
# Typically run via cron

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

LOG_DATE=$(date -u '+%Y-%m-%d')
LOG_FILE="logs/pipeline-${LOG_DATE}.log"
mkdir -p logs

exec > >(tee -a "$LOG_FILE") 2>&1

echo ""
echo "========================================"
echo "EgoistAI Daily Pipeline"
echo "Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"

# Preflight checks
echo ""
echo "--- Preflight ---"

if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js not found"
  exit 1
fi
echo "Node.js: $(node --version)"

if ! command -v git &>/dev/null; then
  echo "ERROR: git not found"
  exit 1
fi

if [ ! -f .env ]; then
  echo "ERROR: .env file not found"
  exit 1
fi
echo "Environment: OK"

# Pull latest
echo ""
echo "--- Git Pull ---"
git pull --rebase || echo "WARNING: git pull failed, continuing..."

# Publish from drafts (2 articles per run)
echo ""
echo "--- Publishing Drafts ---"
bash scripts/publish-from-drafts.sh 2

# Build
echo ""
echo "--- Building ---"
npm run build

# Check if there are changes to commit
if git diff --quiet && git diff --cached --quiet; then
  echo ""
  echo "No changes to commit."
  exit 0
fi

# Commit and push
echo ""
echo "--- Commit & Push ---"
git add -A
ARTICLE_COUNT=$(git diff --cached --name-only | grep -c 'src/content/articles/' || true)
git commit -m "content(auto): publish ${ARTICLE_COUNT} articles ${LOG_DATE}"
git push

echo ""
echo "--- Queue Status ---"
bash scripts/queue-status.sh

echo ""
echo "========================================"
echo "Pipeline completed at $(date -u '+%H:%M:%S UTC')"
echo "========================================"
