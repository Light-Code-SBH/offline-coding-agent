"""
Code Analysis - Python Parser
==============================
Parser and error detector for Python code.

Owner: Member 2 (Code Analysis Lead)
"""

from typing import List
from .base_parser import BaseParser, CodeError, CodeExplanation


class PythonParser(BaseParser):
    """
    Python-specific code parser using tree-sitter and built-in ast module.
    
    TODO (Member 2):
    - Install tree-sitter-python: pip install tree-sitter-python
    - Use Python's built-in `ast` module for initial parsing
    - Use `py_compile` for syntax checking
    - Use `pylint` or custom rules for style/logic checks
    """

    @property
    def language(self) -> str:
        return "python"

    @property
    def file_extensions(self) -> List[str]:
        return [".py"]

    def parse(self, code: str) -> dict:
        """
        Parse Python code into an AST.
        
        Hint: Use Python's built-in `ast` module:
            import ast
            tree = ast.parse(code)
        """
        # TODO: Implement Python AST parsing
        raise NotImplementedError("Member 2: Implement Python parser")

    def detect_errors(self, code: str) -> List[CodeError]:
        """
        Detect errors in Python code.
        
        Approach:
        1. Try ast.parse() — catches syntax errors
        2. Try py_compile — catches more syntax issues
        3. Run custom rules for common bugs (e.g., undefined vars)
        """
        # TODO: Implement Python error detection
        raise NotImplementedError("Member 2: Implement Python error detection")

    def get_line_explanations(self, code: str) -> List[CodeExplanation]:
        """
        Break Python code into logical blocks for explanation.
        
        Hint: Use ast.walk() to identify functions, classes, loops, etc.
        """
        # TODO: Implement Python code block extraction
        raise NotImplementedError("Member 2: Implement Python explanation blocks")

    def detect_language(self, code: str) -> float:
        """Detect if code is Python based on keywords and syntax."""
        python_indicators = ['def ', 'import ', 'print(', 'class ', 'elif ', 
                            'self.', '__init__', 'True', 'False', 'None']
        score = sum(1 for indicator in python_indicators if indicator in code)
        return min(score / 5.0, 1.0)
