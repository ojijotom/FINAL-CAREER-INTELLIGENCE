"""Backend-only OpenAI integration for career guidance."""

import os

from openai import OpenAI, OpenAIError


class AIConfigurationError(Exception):
    """Raised when the AI provider is not configured."""


class AIGenerationError(Exception):
    """Raised when the AI provider cannot generate guidance."""


def is_ai_configured() -> bool:
    """Check whether an OpenAI API key is available."""
    return bool(os.getenv("OPENAI_API_KEY"))


def generate_guidance(prompt: str) -> str:
    """Generate career guidance using OpenAI Responses API."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise AIConfigurationError(
            "AI provider is not configured. Set OPENAI_API_KEY "
            "in the backend environment."
        )

    if not prompt or not prompt.strip():
        raise ValueError("A non-empty guidance prompt is required.")

    try:
        client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=1,
        )

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-6-astra"),
            input=prompt,
            max_output_tokens=1200,
            store=False,
        )

        guidance = response.output_text.strip()

        if not guidance:
            raise AIGenerationError(
                "The AI provider returned an empty response."
            )

        return guidance

    except OpenAIError as exc:
        raise AIGenerationError(
            "AI guidance could not be generated right now. "
            "Please try again later."
        ) from exc
