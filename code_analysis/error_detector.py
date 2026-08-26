"""
Code Analysis - Error Detector
===============================
Orchestrates error detection across all supported languages.

Owner: Member 2 (Code Analysis Lead)
"""

from typing import List, Optional
from .parsers.base_parser import BaseParser, CodeError
from .parsers.python_parser import PythonParser
# TODO: Import other parsers as they're built
# from .parsers.java_parser import JavaParser
# from .parsers.c_parser import CParser
# from .parsers.javascript_parser import JavaScriptParser


class ErrorDetector:
    """
    Main error detection orchestrator.
    
    Routes code to the appropriate language parser and
    combines static analysis with AI-enhanced detection.
    """

    def __init__(self):
        self.parsers = {
            "python": PythonParser(),
            # TODO: Add other parsers
            # "java": JavaParser(),
            # "c": CParser(),
            # "javascript": JavaScriptParser(),
        }

    def detect(self, code: str, language: str) -> List[CodeError]:
        """
        Detect errors in code using the appropriate parser.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            List of detected CodeError objects
        """
        parser = self.parsers.get(language)
        if not parser:
            raise ValueError(f"Unsupported language: {language}. "
                           f"Supported: {list(self.parsers.keys())}")
        
        return parser.detect_errors(code)

    def auto_detect_language(self, code: str) -> Optional[str]:
        """
        Auto-detect the programming language of the given code.
        
        Returns:
            Language name or None if confidence is too low
        """
        best_match = None
        best_score = 0.0

        for lang, parser in self.parsers.items():
            score = parser.detect_language(code)
            if score > best_score:
                best_score = score
                best_match = lang

        return best_match if best_score >= 0.3 else None
