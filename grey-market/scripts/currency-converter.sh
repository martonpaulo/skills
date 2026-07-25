#!/usr/bin/env bash
# currency-converter.sh - converts a foreign-currency amount to BRL using spot rates in exchange-rates.json.
# Usage: bash currency-converter.sh <CURRENCY> <amount>
# Example: bash currency-converter.sh CNY 12
#          bash currency-converter.sh MYR 5.50
# To update rates, edit scripts/exchange-rates.json (rates per currency unit -> BRL).

set -euo pipefail

cd "$(dirname "$0")"

currency="${1:-}"
amount="${2:-}"

if [[ -z "$currency" || -z "$amount" ]]; then
  echo "Usage: $0 <CURRENCY> <amount>" >&2
  exit 1
fi

if [[ ! -f exchange-rates.json ]]; then
  echo "error: exchange-rates.json not found in $(pwd)" >&2
  exit 1
fi

# jq is required. If missing, install it with brew install jq or apt install jq.
if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is not installed" >&2
  exit 1
fi

rate=$(jq -r --arg c "$currency" '.[$c] // empty' exchange-rates.json)
if [[ -z "$rate" ]]; then
  echo "error: currency $currency is not in exchange-rates.json" >&2
  echo "edit $(pwd)/exchange-rates.json and add: \"$currency\": <BRLRate>" >&2
  exit 1
fi

brl=$(awk -v a="$amount" -v r="$rate" 'BEGIN{printf "%.2f", a*r}')
printf "%s %.2f -> BRL %s (rate %s)\n" "$currency" "$amount" "$brl" "$rate"
