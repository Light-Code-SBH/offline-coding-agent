"""
Code Analysis - Base Parser
============================
Abstract base class for language-specific code parsers.

Owner: Member 2 (Code Analysis Lead)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class CodeError:
    """Represents a detected error in code."""

    def __init__(self, line: int, column: int, error_type: str,
                 severity: str, message: str, suggestion: str = None,
                 fixed_code: str = None):
        self.line = line
        self.column = column
        self.error_type = error_type  # syntax, runtime, logic, style
        self.severity = severity      # error, warning, info
        self.message = message
        self.suggestion = suggestion
        self.fixed_code = fixed_code

    def to_dict(self) -> dict:
        return {
            "line": self.line,
            "column": self.column,
            "type": self.error_type,
            "severity": self.severity,
            "message": self.message,
            "suggestion": self.suggestion,
            "fixed_code": self.fixed_code,
        }


class CodeExplanation:
    """Represents an explanation for a code block."""

    def __init__(self, line_start: int, line_end: int, code: str, explanation: str):
        self.line_start = line_start
        self.line_end = line_end
        self.code = code
        self.explanation = explanation

    def to_dict(self) -> dict:
        return {
            "line_start": self.line_start,
            "line_end": self.line_end,
            "code": self.code,
            "explanation": self.explanation,
        }


class BaseParser(ABC):
    """
    Abstract base class that all language parsers must implement.
    
    Member 2 should create subclasses:
    - PythonParser(BaseParser)
    - JavaParser(BaseParser)
    - CParser(BaseParser)
    - JavaScriptParser(BaseParser)
    """

    @property
    @abstractmethod
    def language(self) -> str:
        """Return the language name (e.g., 'python', 'java')."""
        pass

    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """Return supported file extensions (e.g., ['.py'])."""
        pass

    @abstractmethod
    def parse(self, code: str) -> dict:
        """
        Parse source code into an AST or equivalent structure.
        
        Args:
            code: Raw source code string
            
        Returns:
            Parsed representation of the code
        """
        pass

    @abstractmethod
    def detect_errors(self, code: str) -> List[CodeError]:
        """
        Detect errors in the source code using static analysis.
        
        Args:
            code: Raw source code string
            
        Returns:
            List of CodeError objects
        """
        pass

    @abstractmethod
    def get_line_explanations(self, code: str) -> List[CodeExplanation]:
        """
        Break code into logical blocks for explanation.
        
        Args:
            code: Raw source code string
            
        Returns:
            List of CodeExplanation objects (explanation field may be empty,
            to be filled by AI engine)
        """
        pass

    def detect_language(self, code: str) -> float:
        """
        Return a confidence score (0-1) that this code matches our language.
        Used for auto-detection when language is not specified.
        
        Args:
            code: Raw source code string
            
        Returns:
            Confidence score between 0 and 1
        """
        # Default implementation — override for better detection
        return 0.0
