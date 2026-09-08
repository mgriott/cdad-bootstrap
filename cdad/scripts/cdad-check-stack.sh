#!/usr/bin/env bash
# CDAD - stack map freshness gate.
#
# The instruction layer asks agents to keep cdad/context/stack.md current.
# This makes it deterministic: if a change adds or edits an ADR without
# touching the map, the build fails.
#
# Usage:
#   scripts/cdad-check-stack.sh              # compare against origin/main
#   scripts/cdad-check-stack.sh <base-ref>   # compare against another ref
#
# Exit 0 = pass, 1 = violation, 2 = cannot determine.

set -euo pipefail

BASE="${1:-origin/main}"
MAP="cdad/context/stack.md"

if [ ! -f "cdad/.frozen" ]; then
  echo "cdad-check-stack: project is not frozen yet, nothing to enforce."
  exit 0
fi

# --- referential integrity: every ADR cited in the map must exist ---
# Runs unconditionally (governed regime, any invocation) - a dangling
# citation is wrong regardless of whether this diff touched an ADR.
MISSING=""
while read -r adr; do
  [ -z "$adr" ] && continue
  if ! ls "cdad/adr/${adr}"*.md >/dev/null 2>&1; then
    MISSING="$MISSING  $adr\n"
  fi
done < <(grep -oE 'ADR-[0-9]{3}' "$MAP" | sort -u)

if [ -n "$MISSING" ]; then
  echo "cdad-check-stack: FAILED - the map cites ADRs that do not exist:" >&2
  printf "%b" "$MISSING" >&2
  echo "A citation to a file nobody can open is not governance." >&2
  exit 1
fi

# --- drift-signals block presence ---
if ! grep -q '^```cdad-drift-signals' "$MAP"; then
  echo "cdad-check-stack: WARNING - $MAP has no cdad-drift-signals block."
  echo "                  The drift detector cannot operate without it."
  echo "                  This will become a hard failure in a future version."
fi

if ! git rev-parse --verify --quiet "$BASE" >/dev/null; then
  echo "cdad-check-stack: cannot resolve base ref '$BASE'" >&2
  exit 2
fi

CHANGED="$(git diff --name-only "$BASE"...HEAD)"

ADR_CHANGED="$(echo "$CHANGED" | grep -E '^cdad/adr/ADR-[0-9]+' || true)"
MAP_CHANGED="$(echo "$CHANGED" | grep -Fx "$MAP" || true)"

if [ -z "$ADR_CHANGED" ]; then
  echo "cdad-check-stack: no ADR changes, nothing to enforce."
  exit 0
fi

if [ -n "$MAP_CHANGED" ]; then
  echo "cdad-check-stack: ADR change accompanied by a map update."
  echo "$ADR_CHANGED" | sed 's/^/  ADR: /'
  exit 0
fi

cat >&2 <<MSG
cdad-check-stack: FAILED

These ADRs changed without updating $MAP:

$(echo "$ADR_CHANGED" | sed 's/^/  /')

An architectural decision that is not reflected in the stack map is invisible to
everyone who reads the map to understand the system - which is everyone.

Update the map's affected rows and append a row to its change log. If the
decision genuinely does not alter the map, say so in the ADR and add a change
log row recording that.
MSG
exit 1
