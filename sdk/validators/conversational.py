"""Validator for conversational relevance (tangent check)."""

from .base import BaseValidator

class ConversationalValidator(BaseValidator):
    priority: int = 4

    def validate(self, response_text):
        """Validate the conversational relevance of the response text."""
        # TODO: Implement conversational validation (e.g., DistilBERT tangent check)
        print("TODO: Implement ConversationalValidator.validate")
        return response_text, [] # Return original text and empty list of issues for now

