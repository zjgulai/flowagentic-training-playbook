#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx is required. Install the pinned Node dependencies first." >&2
  exit 1
fi

if [[ ! -x node_modules/.bin/playwright-cli ]]; then
  echo "Error: pinned Playwright CLI is missing. Run: npm ci" >&2
  exit 1
fi

exec npx --no-install playwright-cli "$@"
