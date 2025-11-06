#!/usr/bin/env bash#!/bin/bash
#!/usr/bin/env bash
# Pre-commit gitignore review hook (Issue #99 / PR #101)
# Soft warning mode (exit 0). Configure: git config core.hooksPath .githooks
# Optional patterns file: .gitignore_review_patterns (one pattern per line, '#' comments allowed)

set -euo pipefail

BASE_PATTERNS="Bell Textron|Tyeco|Upwork|proprietary|confidential|internal-only"
if [ -f ".gitignore_review_patterns" ]; then
  EXTRA=$(grep -v '^#' .gitignore_review_patterns | tr '\n' '|' | sed 's/|$//') || true
  if [ -n "${EXTRA}" ]; then
    PATTERNS="${BASE_PATTERNS}|${EXTRA}"
  else
    PATTERNS="${BASE_PATTERNS}"
  fi
else
  PATTERNS="${BASE_PATTERNS}"
fi

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "${STAGED_FILES}" ] && exit 0

echo "[gitignore-review] Scanning staged files for sensitive patterns..." >&2
WARNINGS_FOUND=0

for file in ${STAGED_FILES}; do
  # Ignore hook directory itself
  case "$file" in
    .githooks/*) continue ;;
  esac
  [ -f "${file}" ] || continue
  # Simple text heuristic: treat as text if grep can read it without error
  if grep -Iq . "${file}"; then
    if grep -qiE "${PATTERNS}" "${file}" 2>/dev/null; then
      MATCHED=$(grep -ioE "${PATTERNS}" "${file}" | sort -u | tr '\n' ',' | sed 's/,$//')
      echo "WARNING: ${file} contains potentially sensitive content" >&2
      [ -n "${MATCHED}" ] && echo "  Matched: ${MATCHED}" >&2
      echo "  Suggested actions:" >&2
      echo "    - Review and redact if necessary" >&2
      echo "    - Add to .gitignore if file should remain local" >&2
      echo "    - Move to private docs directory" >&2
      WARNINGS_FOUND=1
    fi
  fi
  case "${file}" in
    docs/client_meetings/*)
      echo "💡 Suggest ignoring 'docs/client_meetings/*.md' if internal-only" >&2 ;;
    docs/external_projects/*)
      echo "💡 Suggest verifying external project backups do not contain secrets" >&2 ;;
  esac
done

if [ ${WARNINGS_FOUND} -eq 1 ]; then
  echo "SUMMARY: Sensitive content detected (soft warning, commit not blocked)" >&2
  echo "SUMMARY: To enforce blocking later, change exit 0 -> exit 1" >&2
fi

exit 0
for file in $STAGED_FILES; do      echo "💡 Suggest adding 'docs/client_meetings/*.md' to .gitignore if internal-only" >&2 ;;
