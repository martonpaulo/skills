"""AST validation for documentation-only sandbox programs."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    is_safe: bool
    errors: list[str] = field(default_factory=list)


class CodeValidator:
    BLOCKED = {
        "__import__", "breakpoint", "compile", "delattr", "dir", "eval", "exec",
        "getattr", "globals", "hasattr", "input", "locals", "open", "setattr", "vars",
    }

    def __init__(self, max_code_length: int = 10_000):
        self.max_code_length = max_code_length

    def validate(self, code: str) -> ValidationResult:
        if not isinstance(code, str) or not code.strip():
            return ValidationResult(False, ["Code must be a non-empty string"])
        if len(code) > self.max_code_length:
            return ValidationResult(False, [f"Code exceeds {self.max_code_length} characters"])
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as exc:
            return ValidationResult(False, [f"Syntax error at line {exc.lineno}: {exc.msg}"])

        errors = []
        has_result = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                errors.append("Imports are not allowed")
            elif isinstance(node, ast.Name):
                if node.id in self.BLOCKED:
                    errors.append(f"Name '{node.id}' is not allowed")
                if node.id.startswith("__") and node.id.endswith("__"):
                    errors.append(f"Dunder name '{node.id}' is not allowed")
            elif isinstance(node, ast.Attribute) and node.attr.startswith("__") and node.attr.endswith("__"):
                errors.append(f"Dunder attribute '{node.attr}' is not allowed")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in self.BLOCKED:
                    errors.append(f"Call to '{node.func.id}' is not allowed")
                if isinstance(node.func, ast.Attribute) and node.func.attr in self.BLOCKED:
                    errors.append(f"Call to '{node.func.attr}' is not allowed")
            elif isinstance(node, ast.Assign):
                has_result |= any(isinstance(target, ast.Name) and target.id == "result" for target in node.targets)
            elif isinstance(node, ast.AnnAssign):
                has_result |= isinstance(node.target, ast.Name) and node.target.id == "result"
        if not has_result:
            errors.append("Code must assign the final JSON-serializable value to 'result'")
        return ValidationResult(not errors, sorted(set(errors)))
