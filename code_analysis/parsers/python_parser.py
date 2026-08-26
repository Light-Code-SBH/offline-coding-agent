"""
Code Analysis - Python Parser
==============================
Parser and error detector for Python code.

Owner: Member 2 (Code Analysis Lead)
"""

import ast
from typing import List
from .base_parser import BaseParser, CodeError, CodeExplanation


class PythonParser(BaseParser):
    """
    Python-specific code parser using the built-in ast module.
    """

    @property
    def language(self) -> str:
        return "python"

    @property
    def file_extensions(self) -> List[str]:
        return [".py"]

    def parse(self, code: str) -> dict:
        """
        Parse Python code into an AST and return basic structural info.
        """
        tree = ast.parse(code)
        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        imports = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                imports.extend(alias.name for alias in n.names)
            elif isinstance(n, ast.ImportFrom):
                imports.append(n.module)

        return {
            "tree": tree,
            "functions": functions,
            "classes": classes,
            "imports": imports,
        }

    def detect_errors(self, code: str) -> List[CodeError]:
        """
        Detect errors in Python code.

        Layer 1: ast.parse() catches syntax errors.
        Layer 2: Custom checks for common issues (undefined names at
                 module level via NameError simulation is out of scope
                 for static analysis without execution, so we focus on
                 straightforward static checks: unused imports, bare
                 except clauses, and mutable default arguments).
        """
        errors: List[CodeError] = []

        # Layer 1 — syntax errors
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            errors.append(CodeError(
                line=e.lineno or 0,
                column=e.offset or 0,
                error_type="syntax",
                severity="error",
                message=str(e.msg),
            ))
            return errors  # can't run further checks on unparseable code

        # Layer 2 — simple static checks
        lines = code.splitlines()

        # Unused imports (very basic: name never appears again in the code)
        imported_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.append((alias.asname or alias.name.split(".")[0], node.lineno))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.append((alias.asname or alias.name, node.lineno))

        for name, lineno in imported_names:
            occurrences = sum(1 for line in lines if name in line)
            if occurrences <= 1:  # only appears on the import line itself
                errors.append(CodeError(
                    line=lineno,
                    column=0,
                    error_type="style",
                    severity="warning",
                    message=f"Unused import: '{name}'",
                    suggestion=f"Remove unused import '{name}' if not needed.",
                ))

        # Bare except clauses
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                errors.append(CodeError(
                    line=node.lineno,
                    column=node.col_offset,
                    error_type="style",
                    severity="warning",
                    message="Bare 'except:' clause catches all exceptions, including system-exiting ones.",
                    suggestion="Catch a specific exception type, e.g. 'except Exception:'.",
                ))

        # Mutable default arguments
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        errors.append(CodeError(
                            line=node.lineno,
                            column=node.col_offset,
                            error_type="logic",
                            severity="warning",
                            message=f"Function '{node.name}' uses a mutable default argument.",
                            suggestion="Use 'None' as the default and initialize the mutable value inside the function body.",
                        ))

        return errors

    def get_line_explanations(self, code: str) -> List[CodeExplanation]:
        """
        Break Python code into logical blocks (functions, classes, top-level
        statements) for explanation. The 'explanation' field is left empty
        here — it's filled in later by the AI engine.
        """
        explanations: List[CodeExplanation] = []
        lines = code.splitlines()

        try:
            tree = ast.parse(code)
        except SyntaxError:
            # If code doesn't parse, fall back to one block covering everything
            return [CodeExplanation(
                line_start=1,
                line_end=len(lines),
                code=code,
                explanation="",
            )]

        for node in tree.body:
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            block_code = "\n".join(lines[start - 1:end])
            explanations.append(CodeExplanation(
                line_start=start,
                line_end=end,
                code=block_code,
                explanation="",
            ))

        return explanations

    def detect_language(self, code: str) -> float:
        """Detect if code is Python based on keywords and syntax."""
        python_indicators = ['def ', 'import ', 'print(', 'class ', 'elif ',
                            'self.', '__init__', 'True', 'False', 'None']
        score = sum(1 for indicator in python_indicators if indicator in code)
        return min(score / 5.0, 1.0)