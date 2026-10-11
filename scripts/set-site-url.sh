#!/usr/bin/env bash
# Swap the site's address (used in canonical, Open Graph, JSON-LD, sitemap,
# robots.txt and the form's no-JS thank-you redirect) in every file at once.
# Usage (no trailing slash):
#   ./scripts/set-site-url.sh https://www.jcpdesign.com
# That replaces the current address (https://apnpapnu.github.io/jcp-design-site).
# To replace some other address:  ./scripts/set-site-url.sh NEW_URL OLD_URL
set -euo pipefail
cd "$(dirname "$0")/.."
NEW="${1:?Give the new site URL, e.g. https://yourname.github.io/jcp-design-site}"
OLD="${2:-https://apnpapnu.github.io/jcp-design-site}"
NEW="${NEW%/}"
FILES=$(grep -rl --exclude-dir=.git --exclude-dir=scripts --exclude=README.md -F "$OLD" . || true)
if [ -z "$FILES" ]; then echo "Nothing to replace ($OLD not found)."; exit 0; fi
for f in $FILES; do
  sed -i.bak "s#${OLD}#${NEW}#g" "$f" && rm -f "$f.bak"
  echo "updated $f"
done
