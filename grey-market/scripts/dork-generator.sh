#!/usr/bin/env bash
# dork-generator.sh - generates Google/Bing `site:` dorks per target domain for grey-market research.
# STRINGS ONLY — does NOT search. Pipe each line into a search engine or anysearch.py to execute.
#
# Usage:
#   bash dork-generator.sh "<query>" [domain...]
#   bash dork-generator.sh --search "<query>" [domain...]   # generate + execute via anysearch.py
#
# Examples:
#   bash dork-generator.sh "windows 11 pro key" reddit.com cheapgamekeys.com
#   bash dork-generator.sh --search "chatgpt plus account" g2g.com epicnpc.com
#
# --search delegates each dork to scripts/anysearch.py (needs ANYSEARCH_API_KEY).
# Default domains used when none given: edit DEFAULTS below.

set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"

DEFAULTS="reddit.com lowendtalk.com blackhatworld.com plati.market 52pojie.cn v2ex.com desidime.com mipped.com epicnpc.com hostloc.com nodeseek.com forum.lowyat.net ggmax.com.br desapegogames.com.br gamemarket.com.br promobit.com.br pelando.com.br hardmob.com.br"

# Parse --search flag if present as the first arg.
do_search=0
if [[ "${1:-}" == "--search" ]]; then
  do_search=1
  shift
fi

query="${1:-}"
shift || true
domains="${*:-$DEFAULTS}"

if [[ -z "$query" ]]; then
  echo "Usage: $0 [--search] \"<query>\" [domain...]" >&2
  exit 1
fi

if [[ "$do_search" -eq 1 ]]; then
  if [[ ! -f "$script_dir/anysearch.py" ]]; then
    echo "error: anysearch.py not found next to this script ($script_dir)" >&2
    exit 1
  fi
  py_bin="python3"
  command -v "$py_bin" >/dev/null 2>&1 || py_bin="python"
  for d in $domains; do
    dork="site:$d $query"
    echo "=== $dork ===" >&2
    "$py_bin" "$script_dir/anysearch.py" "$dork" --max_results 10 --format markdown || true
  done
  exit 0
fi

year="$(date +%Y)"

for d in $domains; do
  echo "site:$d \"$query\""
  echo "site:$d \"$query\" $year"   # current-year variant, to surface fresh threads
done
