#!/bin/bash
# Sync script: cleans up any stale git locks, commits everything, and pushes
# to the "develop" branch. Vercel deploys this as a PREVIEW, not production,
# so "main"/production stays untouched until you promote a preview yourself
# in the Vercel dashboard (or merge develop -> main when you're ready to go live).
#
# Usage: ./sync.sh "beschrijving van de wijzigingen"
# Het commit-bericht is verplicht, zodat elke deployment in Vercel duidelijk
# laat zien wat er is aangepast (in plaats van alleen een tijdstip).

set -e

cd "$(dirname "$0")"

if [ -z "$1" ]; then
  echo "Fout: geef een omschrijving van de wijzigingen mee, bv:"
  echo "  ./sync.sh \"Instagram + Facebook iconen in footer\""
  exit 1
fi

MESSAGE="$1"

# Ruim eventuele achtergebleven lockbestanden op (kan gebeuren na een sessie van Claude)
rm -f .git/index.lock .git/HEAD.lock 2>/dev/null || true

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
