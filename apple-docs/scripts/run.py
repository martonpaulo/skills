#!/usr/bin/env python3
"""Run a small Apple documentation query in the restricted sandbox."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import apis
from sandbox import SandboxExecutor


def create_api_handlers() -> dict:
    return {name: getattr(apis, name) for name in apis.__all__}


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute a restricted Apple documentation query")
    parser.add_argument("code", help="Python code that assigns a JSON-serializable value to result")
    parser.add_argument("--project-path", default=".", help="Repository root available to read-only context detection")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    project_root = Path(args.project_path).expanduser().resolve()
    if not project_root.is_dir():
        print(json.dumps({"success": False, "error": "project path is not a directory"}))
        return 2
    apis.configure(project_root)
    executor = SandboxExecutor(timeout=args.timeout, api_handlers=create_api_handlers())
    output = executor.execute(args.code).to_dict()
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if output.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
