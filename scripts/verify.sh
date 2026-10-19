#!/usr/bin/env bash
#
# verify.sh — run the same grader CI runs, on your own machine.
#
#   ./scripts/verify.sh --section dockerfile --path lab-01
#   ./scripts/verify.sh --section compose    --path lab-01 --keep
#
# This is a thin wrapper. The checks themselves live in the course's grader repository
# at a fixed tag, which is also what the pipeline uses — so a green run here means a
# green check there. You cannot edit the checks, and you are not meant to: being handed
# the grader in advance is the point.
set -euo pipefail

REPO="${CATSHOP_GRADER_REPO:-kse-ci-cd-basics-course/catshop-grader}"
REF="${CATSHOP_GRADER_REF:-v1}"

command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
command -v docker >/dev/null || { echo "docker is required, and must be running" >&2; exit 1; }

CACHE="${TMPDIR:-/tmp}/catshop-grader-$REF"
if [ -d "$CACHE/.git" ]; then
  git -C "$CACHE" fetch --quiet --depth 1 origin "$REF" 2>/dev/null || true
  git -C "$CACHE" checkout --quiet "FETCH_HEAD" 2>/dev/null || true
else
  rm -rf "$CACHE"
  git clone --quiet --depth 1 --branch "$REF" "https://github.com/$REPO.git" "$CACHE" \
    || { echo "could not fetch $REPO at $REF — is the tag published, and can you read the repo?" >&2; exit 1; }
fi

exec bash "$CACHE/verify/verify.sh" "$@"
