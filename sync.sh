#!/bin/bash
# Sync script: cleans up any stale git locks, commits everything, and pushes.
# Usage: ./sync.sh ["optioneel commit bericht"]

set -e

cd "$(dirname "$0")"

# Ruim eventuele achtergebleven lockbestanden op (kan gebeuren na een sessie van Claude)
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null || true

MESSAGE="${1:-update $(date '+%Y-%m-%d %H:%M')}"

git add -A

if git diff --cached --quiet; then
  echo "Geen wijzigingen om te committen."
else
  git commit -m "$MESSAGE"
fi

git push
