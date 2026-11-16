"""AI-provider boundary. No external AI calls are made yet."""

import os


class AIConfigurationError(Exception):
    """Raised when the AI provider is not configured."""


def is_ai_configured() -> bool:
    """Check whether an AI provider key is available on the backend."""
    return bool(os.getenv("OPENAI_API_KEY"))


def generate_guidance(prompt: str) -> str:
    """
    Placeholder for the future AI provider integration.

    The API key must remain in the backend environment.
    This function deliberately does not make an external API call yet.
    """
    if not is_ai_configured():
        raise AIConfigurationError(
            "AI provider is not configured. Set OPENAI_API_KEY "
            "in the backend environment before enabling AI guidance."
        )

    raise NotImplementedError(
        "The AI provider client will be implemented in the next phase."
    )
