#!/usr/bin/env python3
# anysearch.py - calls the AnySearch API (/v1/search) for grey-market sweeps.
# Dependencies: Python stdlib only (urllib). No requests, no pip install.
# Usage: python anysearch.py "<query>" [--max_results N] [--tag TAG] [--zone cn|intl]
#        [--language LANG] [--params JSON] [--format json|markdown]
# Example: python anysearch.py "windows 11 pro key cheap" --max_results 10 --tag general.general
#          python anysearch.py "netflix account sharing" --language zh-CN --zone cn
#
# ANYSEARCH_API_KEY resolution order:
#   1. .env in the skill directory (sibling of scripts/)
#   2. .env in the current working directory (cwd)
#   3. ANYSEARCH_API_KEY environment variable
# If no key is found, the script prints a warning and exits with code 1.

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.anysearch.com/v1/search"
ENV_KEY = "ANYSEARCH_API_KEY"


def parse_env(path):
    """Read a simple .env file (KEY=VALUE, ignoring comments and blank lines)."""
    out = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k:
                    out[k] = v
    except (OSError, IOError):
        return None
    return out


def resolve_api_key():
    """Return (key, source) or (None, None) when no key is found."""
    # 1. .env in the skill directory (sibling of scripts/)
    skill_env = os.path.join(os.path.dirname(__file__), "..", ".env")
    data = parse_env(skill_env)
    if data and data.get(ENV_KEY):
        return data[ENV_KEY], f"skill .env ({os.path.abspath(skill_env)})"

    # 2. .env in the current working directory
    cwd_env = os.path.join(os.getcwd(), ".env")
    data = parse_env(cwd_env)
    if data and data.get(ENV_KEY):
        return data[ENV_KEY], f"cwd .env ({os.path.abspath(cwd_env)})"

    # 3. environment variable
    env_val = os.environ.get(ENV_KEY)
    if env_val:
        return env_val, "environment variable"

    return None, None


def search(query, api_key, max_results=10, tag=None, zone=None,
           language=None, params=None, fmt="json"):
    """POST /v1/search and return the decoded response body."""
    body = {"query": query, "max_results": max_results, "format": fmt}
    if tag:
        body["tag"] = tag
    if zone:
        body["zone"] = zone
    if language:
        body["language"] = language
    if params:
        if isinstance(params, str):
            try:
                body["params"] = json.loads(params)
            except json.JSONDecodeError as e:
                print(f"error: invalid --params JSON: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            body["params"] = params

    payload = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(API_BASE, data=payload, headers=headers,
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP error {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"network error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    if fmt == "markdown":
        return raw
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def main():
    p = argparse.ArgumentParser(
        description="Grey-market sweep via AnySearch /v1/search")
    p.add_argument("query", help="search term")
    p.add_argument("--max_results", type=int, default=10,
                   help="1-20, default 10")
    p.add_argument("--tag", default=None,
                   help="sub-domain {domain}.{sub_domain}, example: general.general")
    p.add_argument("--zone", choices=["cn", "intl"], default=None,
                   help="region")
    p.add_argument("--language", default=None,
                   help="preferred language, example: zh-CN, en, pt-BR")
    p.add_argument("--params", default=None,
                   help='extended JSON, example: \'{"library":"golang"}\'')
    p.add_argument("--format", choices=["json", "markdown"], default="json",
                   help="output format")
    args = p.parse_args()

    api_key, source = resolve_api_key()
    if not api_key:
        print(
            "WARNING: ANYSEARCH_API_KEY was not found.\n"
            "A free AnySearch account is required to use this helper.\n"
            "Create a key at https://anysearch.com/console/api-keys and configure "
            "ANYSEARCH_API_KEY:\n"
            "  - in the skill directory .env, or\n"
            "  - in the current working directory .env, or\n"
            "  - as an environment variable in the current shell.",
            file=sys.stderr)
        sys.exit(1)

    print(f"# key source: {source}", file=sys.stderr)

    result = search(args.query, api_key,
                    max_results=args.max_results, tag=args.tag,
                    zone=args.zone, language=args.language,
                    params=args.params, fmt=args.format)

    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
