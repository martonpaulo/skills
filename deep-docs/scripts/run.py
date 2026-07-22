#!/usr/bin/env python3
"""Run a version-aware documentation query in the restricted sandbox."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import registry
from sandbox import SandboxExecutor


def _source(value: str) -> dict:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"source must be a JSON object: {exc.msg}") from exc
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("source must be a JSON object")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute a restricted documentation query")
    parser.add_argument("code", help="Python code that assigns a JSON-serializable value to result")
    parser.add_argument("--project-path", default=".", help="Repository root for read-only version detection")
    parser.add_argument(
        "--source", action="append", default=[], type=_source,
        help='Explicit source JSON, for example {"name":"docs","provider":"llms_txt","source":"https://example.com/llms.txt","product":"Example"}',
    )
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_path).expanduser().resolve()
    if not root.is_dir():
        print(json.dumps({"success": False, "error": "project path is not a directory"}))
        return 2
    try:
        registry.configure(str(root), args.source)
    except ValueError as exc:
        print(json.dumps({"success": False, "error": str(exc)}))
        return 2
    handlers = {name: getattr(registry, name) for name in registry.PUBLIC_APIS}
    output = SandboxExecutor(timeout=args.timeout, api_handlers=handlers).execute(args.code).to_dict()
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if output.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
