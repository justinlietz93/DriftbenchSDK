"""Unit tests for the SyntaxValidator."""

import pytest
from sdk.validators.syntax import SyntaxValidator

def test_valid_code():
    """Test that valid Python code passes validation."""
    validator = SyntaxValidator()
    response = {"code": "def hello():\n    print(\"Hello, world!\")"}
    prompt = "Write a hello world function"
    _, error = validator.validate(response, prompt)
    assert error is None

def test_invalid_code():
    """Test that invalid Python code returns the correct error dictionary."""
    validator = SyntaxValidator()
    # Invalid code as specified in the task list
    response = {"code": "def foo(\n  pass"}
    prompt = "Write an incomplete function"
    _, error = validator.validate(response, prompt)

    assert error is not None
    assert error["error"] == "Syntax error"
    # ast.parse reports the line where the error *ends* or is detected
    # For "def foo(\n  pass", the error is detected at line 2 (unexpected EOF)
    assert error["line"] == 1
    assert error["fix"] == "fix syntax"
    assert error["confidence"] == 1.0

def test_no_code_field():
    """Test behavior when the 'code' field is missing."""
    validator = SyntaxValidator()
    response = {"text": "Some explanation without code."}
    prompt = "Explain something"
    _, error = validator.validate(response, prompt)
    # Current implementation passes if 'code' is missing
    assert error is None

def test_non_string_code_field():
    """Test behavior when the 'code' field is not a string."""
    validator = SyntaxValidator()
    response = {"code": ["def foo(): pass"]}
    prompt = "Write a function"
    _, error = validator.validate(response, prompt)
    assert error is not None
    assert error["error"] == "Invalid code type"
    assert error["fix"] == "Expected string for 'code', got list"
    assert error["confidence"] == 1.0

