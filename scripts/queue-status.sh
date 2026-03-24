#!/usr/bin/env bash
set -euo pipefail

# Show draft queue status and estimated depletion date
# Usage: bash scripts/queue-status.sh

DRAFTS_DIR="src/content/drafts"
ARTICLES_DIR="src/content/articles"
DAILY_RATE=4

echo "=== EgoistAI Queue Status ==="
echo ""

# Count drafts and articles
DRAFT_COUNT=$(find "$DRAFTS_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
ARTICLE_COUNT=$(find "$ARTICLES_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

echo "Published articles: $ARTICLE_COUNT"
echo "Queued drafts:      $DRAFT_COUNT"
echo "Daily publish rate:  $DAILY_RATE articles/day"
echo ""

if [ "$DRAFT_COUNT" -eq 0 ]; then
  echo "WARNING: Draft queue is EMPTY! Generate more articles."
  exit 0
fi

# Calculate days until depletion
DAYS_LEFT=$(( (DRAFT_COUNT + DAILY_RATE - 1) / DAILY_RATE ))

# Calculate depletion date
if [[ "$(uname)" == "Darwin" ]]; then
  DEPLETION_DATE=$(date -v+"${DAYS_LEFT}d" '+%Y-%m-%d')
else
  DEPLETION_DATE=$(date -d "+${DAYS_LEFT} days" '+%Y-%m-%d')
fi

echo "Estimated days of content: $DAYS_LEFT"
echo "Estimated depletion date:  $DEPLETION_DATE"
echo ""

# Show breakdown by category
echo "--- Drafts by Category ---"
for cat_dir in "$DRAFTS_DIR"/*/; do
  if [ -d "$cat_dir" ]; then
    CAT_NAME=$(basename "$cat_dir")
    CAT_COUNT=$(find "$cat_dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [ "$CAT_COUNT" -gt 0 ]; then
      echo "  $CAT_NAME: $CAT_COUNT"
    fi
  fi
done
echo ""
