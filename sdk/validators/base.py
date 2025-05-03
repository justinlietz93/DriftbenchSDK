"""Base class for all validators."""

from abc import ABC, abstractmethod

class Validator(ABC):
    """Abstract base class for all validators."""
    priority: int = 99 # Default priority, should be overridden by subclasses

    @abstractmethod
    def validate(self, response: dict, prompt: str) -> tuple[dict, dict | None]:
        """Validate the response.

        Args:
            response: The response dictionary, expected to contain keys like 'code'.
            prompt: The original prompt string.

        Returns:
            A tuple containing:
            - The potentially modified response dictionary.
            - An error dictionary if validation fails, otherwise None.
              Error dict format: {"error": str, "line": int|None, "fix": str|None, "confidence": float}
        """
        pass

