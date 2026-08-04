#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

cli="$repo_root/scripts/playwright_cli.sh"
workflow="$repo_root/scripts/browser_smoke_workflow.js"
output_dir="${PLAYBOOK_SMOKE_OUTPUT_DIR:-$repo_root/output/playwright}"
port="${PLAYBOOK_SMOKE_PORT:-8765}"
base_url="http://127.0.0.1:${port}"
server_log="$output_dir/site-server.log"
server_pid=""
sessions_to_close=""

run_cli() {
  bash "$cli" "$@"
}

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM
  for session in $sessions_to_close; do
    run_cli -s="$session" close >/dev/null 2>&1 || true
  done
  if [[ -n "$server_pid" ]] && kill -0 "$server_pid" >/dev/null 2>&1; then
    kill "$server_pid" >/dev/null 2>&1 || true
    wait "$server_pid" >/dev/null 2>&1 || true
  fi
  if [[ "$exit_code" -eq 0 ]]; then
    rm -rf "$repo_root/.playwright-cli"
  fi
  exit "$exit_code"
}
trap cleanup EXIT INT TERM

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required to serve the built site." >&2
  exit 1
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is required to probe the local site." >&2
  exit 1
fi
if [[ ! -f "$cli" ]]; then
  echo "Error: Playwright CLI wrapper is missing: $cli" >&2
  exit 1
fi
if [[ ! -f "$workflow" ]]; then
  echo "Error: browser workflow is missing: $workflow" >&2
  exit 1
fi
if [[ ! -f "$repo_root/site/index.html" ]]; then
  echo "Error: built site is missing. Run: uv run mkdocs build --strict" >&2
  exit 1
fi
if [[ ! -f "$repo_root/site/assets/downloads/flowagentic-playbook.pdf" ]]; then
  echo "Error: site PDF is missing. Run scripts/build_pdf.py before browser smoke." >&2
  exit 1
fi

mkdir -p "$output_dir"
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$repo_root/site" \
  >"$server_log" 2>&1 &
server_pid=$!

site_ready=0
attempt=0
sleep 0.1
while [[ "$attempt" -lt 60 ]]; do
  attempt=$((attempt + 1))
  if ! kill -0 "$server_pid" >/dev/null 2>&1; then
    break
  fi
  if curl --fail --silent --show-error --max-time 2 "$base_url/" >/dev/null 2>&1; then
    site_ready=1
    break
  fi
  sleep 0.1
done
if [[ "$site_ready" -ne 1 ]]; then
  echo "Error: local site server did not become ready at $base_url" >&2
  sed -n '1,120p' "$server_log" >&2 || true
  exit 1
fi

browsers="${PLAYBOOK_BROWSERS:-chrome firefox}"
browser_count=0
for browser in $browsers; do
  browser_count=$((browser_count + 1))
  case "$browser" in
    chrome|firefox) ;;
    *)
      echo "Error: unsupported browser '$browser'; allowed: chrome firefox" >&2
      exit 1
      ;;
  esac

  session="playbook-smoke-$$-$browser"
  sessions_to_close="$sessions_to_close $session"
  browser_log="$output_dir/$browser.log"
  echo "Running Playbook browser smoke: $browser"

  if ! run_cli -s="$session" open "$base_url/" --browser="$browser" \
    >"$browser_log" 2>&1; then
    sed -n '1,240p' "$browser_log" >&2
    exit 1
  fi
  if ! run_cli -s="$session" run-code --filename="$workflow" \
    >>"$browser_log" 2>&1; then
    sed -n '1,320p' "$browser_log" >&2
    exit 1
  fi
  if grep -Fq "### Error" "$browser_log" || \
    ! grep -Eq '"status"[[:space:]]*:[[:space:]]*"passed"' "$browser_log"; then
    echo "Error: $browser browser workflow did not produce an explicit pass." >&2
    sed -n '1,320p' "$browser_log" >&2
    exit 1
  fi
  run_cli -s="$session" close >>"$browser_log" 2>&1
  echo "$browser: passed"
done

if [[ "$browser_count" -eq 0 ]]; then
  echo "Error: PLAYBOOK_BROWSERS must name at least one browser." >&2
  exit 1
fi

echo "Playbook browser smoke passed for: $browsers"
