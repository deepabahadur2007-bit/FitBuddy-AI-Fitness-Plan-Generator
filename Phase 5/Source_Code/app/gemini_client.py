from functools import lru_cache

from .config import get_settings


@lru_cache
def get_client():

    settings = get_settings()

    if not settings.gemini_api_key:
        return None

    from google import genai

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    model: str,
    max_output_tokens: int = 5000,
) -> str:

    client = get_client()

    if client is None:
        raise RuntimeError(
            "Gemini API key is not configured."
        )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "temperature": 0.7,
            "max_output_tokens": max_output_tokens,
        },
    )

    text = getattr(
        response,
        "text",
        None,
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()