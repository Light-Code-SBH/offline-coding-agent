"""
Tests - Sample Unit Tests
==========================
Starter unit tests for the project.

Owner: Member 5 (QA & DevOps Lead)
"""

import pytest
from code_analysis.parsers.python_parser import PythonParser
from code_analysis.error_detector import ErrorDetector


class TestPythonParser:
    """Unit tests for the Python parser."""

    def setup_method(self):
        self.parser = PythonParser()

    def test_language_property(self):
        assert self.parser.language == "python"

    def test_file_extensions(self):
        assert ".py" in self.parser.file_extensions

    def test_detect_language_python_code(self):
        code = """
def hello():
    print("Hello, World!")
    
class MyClass:
    def __init__(self):
        self.value = True
"""
        score = self.parser.detect_language(code)
        assert score > 0.5, "Should detect Python with high confidence"

    def test_detect_language_non_python(self):
        code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
"""
        score = self.parser.detect_language(code)
        assert score < 0.3, "Should have low confidence for Java code"

    @pytest.mark.skip(reason="TODO: Implement parse() first")
    def test_parse_valid_code(self):
        code = "x = 1 + 2"
        result = self.parser.parse(code)
        assert result is not None

    @pytest.mark.skip(reason="TODO: Implement detect_errors() first")
    def test_detect_syntax_error(self):
        code = "def foo(\n    print('hello')"  # Missing closing paren
        errors = self.parser.detect_errors(code)
        assert len(errors) > 0
        assert errors[0].error_type == "syntax"


class TestErrorDetector:
    """Unit tests for the error detection orchestrator."""

    def setup_method(self):
        self.detector = ErrorDetector()

    def test_supported_languages(self):
        assert "python" in self.detector.parsers

    def test_unsupported_language_raises(self):
        with pytest.raises(ValueError, match="Unsupported language"):
            self.detector.detect("code", "ruby")

    def test_auto_detect_python(self):
        code = "import os\ndef main():\n    print('hello')"
        lang = self.detector.auto_detect_language(code)
        assert lang == "python"


# ============================================================
# TODO (Member 5): Add more test classes as modules are built
# ============================================================
# class TestJavaParser: ...
# class TestCParser: ...
# class TestJavaScriptParser: ...
# class TestInferencePipeline: ...
# class TestModelManager: ...
# class TestAPIEndpoints: ...
