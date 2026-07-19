#!/bin/bash
# Sync script: cleans up any stale git locks, commits everything, and pushes
# to the "develop" branch. Vercel deploys this as a PREVIEW, not production,
# so "main"/production stays untouched until you promote a preview yourself
# in the Vercel dashboard (or merge develop -> main when you're ready to go live).
#
# Usage: ./sync.sh ["optioneel commit bericht"]

set -e

cd "$(dirname "$0")"

# Ruim eventuele achtergebleven lockbestanden op (kan gebeuren na een sessie van Claude)
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null || true

MESSAGE="${1:-update $(date '+%Y-%m-%d %H:%M')}"

# Zorg dat we altijd op de develop-branch werken (nooit direct op main/productie)
git checkout develop 2>/dev/null || git checkout -b develop

git add -A

if git diff --cached --quiet; then
  echo "Geen wijzigingen om te committen."
else
  git commit -m "$MESSAGE"
fi

git push -u origin develop

echo ""
echo "Gepusht naar 'develop'. Vercel maakt hier een preview-deployment van."
echo "Check je Vercel dashboard en klik 'Promote to Production' zodra je live wilt."
