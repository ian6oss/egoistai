#!/usr/bin/env bash
set -euo pipefail

# Publish N articles from drafts to articles directory
# Usage: bash scripts/publish-from-drafts.sh [count]
# Default: 2 articles

COUNT="${1:-2}"
DRAFTS_DIR="src/content/drafts"
ARTICLES_DIR="src/content/articles"
TODAY=$(date -u '+%Y-%m-%d')
PUBLISHED=0

echo "=== EgoistAI Draft Publisher ==="
echo "Date: $TODAY"
echo "Target: $COUNT articles"
echo ""

# Find all draft markdown files, sorted alphabetically (ensures category distribution)
DRAFT_FILES=$(find "$DRAFTS_DIR" -name "*.md" -type f 2>/dev/null | sort || true)

if [ -z "$DRAFT_FILES" ]; then
  echo "WARNING: No drafts available to publish."
  exit 0
fi

TOTAL_DRAFTS=$(echo "$DRAFT_FILES" | wc -l | tr -d ' ')
echo "Available drafts: $TOTAL_DRAFTS"
echo ""

# Process up to COUNT files
while IFS= read -r draft_file; do
  if [ "$PUBLISHED" -ge "$COUNT" ]; then
    break
  fi

  FILENAME=$(basename "$draft_file")

  # Ensure target articles directory exists
  mkdir -p "$ARTICLES_DIR"

  # Copy file to articles (flat structure, no category subdirs)
  TARGET="$ARTICLES_DIR/$FILENAME"
  cp "$draft_file" "$TARGET"

  # Update date to today
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s/^date: .*/date: \"$TODAY\"/" "$TARGET"
  else
    sed -i "s/^date: .*/date: \"$TODAY\"/" "$TARGET"
  fi

  # Remove the draft
  rm "$draft_file"

  PUBLISHED=$((PUBLISHED + 1))
  echo "[$PUBLISHED] Published: $FILENAME"

done <<< "$DRAFT_FILES"

echo ""
echo "=== Summary ==="
echo "Published: $PUBLISHED articles"
REMAINING=$(find "$DRAFTS_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "Remaining drafts: $REMAINING"

if [ "$REMAINING" -eq 0 ]; then
  echo ""
  echo "WARNING: Drafts queue is now empty!"
fi
