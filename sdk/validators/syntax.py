"""Validator for syntax correctness using ast.parse."""

import ast
from .base import Validator

class SyntaxValidator(Validator):
    """Validates Python code syntax using the built-in ast module."""
    priority: int = 1

    def validate(self, response: dict, prompt: str) -> tuple[dict, dict | None]:
        """Validate the syntax of the code in the response.

        Args:
            response: The response dictionary, expected to contain a key 'code'.
            prompt: The original prompt string (unused in this validator).

        Returns:
            A tuple containing:
            - The original response dictionary.
            - An error dictionary if validation fails (SyntaxError), otherwise None.
        """
        code_to_validate = response.get("code")

        if code_to_validate is None:
            # If no code is present, consider it a different kind of issue or pass?
            # For now, let's assume it passes syntax validation if no code is provided.
            # Alternatively, return an error indicating missing code.
            # error = {
            #     "error": "Missing code field",
            #     "line": None,
            #     "fix": "Ensure response includes a 'code' field",
            #     "confidence": 1.0
            # }
            # return response, error
            return response, None # Assuming pass if no code

        if not isinstance(code_to_validate, str):
            error = {
                "error": "Invalid code type",
                "line": None,
                "fix": f"Expected string for 'code', got {type(code_to_validate).__name__}",
                "confidence": 1.0
            }
            return response, error

        try:
            ast.parse(code_to_validate)
            # If parsing succeeds, syntax is valid
            return response, None
        except SyntaxError as e:
            # If parsing fails, capture the syntax error details
            error = {
                "error": "Syntax error",
                "line": e.lineno,
                "fix": "fix syntax", # Generic fix suggestion as requested
                "confidence": 1.0 # High confidence as it's a direct parser error
            }
            return response, error
        except Exception as e:
            # Catch other potential errors during parsing, though less common
            error = {
                "error": f"Unexpected parsing error: {type(e).__name__}",
                "line": getattr(e, 'lineno', None), # Try to get line number if available
                "fix": "Review code for potential issues beyond basic syntax",
                "confidence": 0.8 # Lower confidence as it's unexpected
            }
            return response, error

