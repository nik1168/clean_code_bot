import os
from openai import OpenAI

# Models that hit a good balance of quality vs cost/speed.
# TODO: let users override these via CLI flag or env var
MODELS = {
    "openai": "gpt-4o-mini",
    "groq": "llama-3.3-70b-versatile",
}

BASE_URLS = {
    "openai": None,  # uses the SDK default
    "groq": "https://api.groq.com/openai/v1",
}

ENV_KEYS = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
}


class ProviderError(Exception):
    pass


def _get_client(provider):
    env_var = ENV_KEYS[provider]
    api_key = os.environ.get(env_var)
    if not api_key:
        raise ProviderError(
            f"Missing API key. Set {env_var} in your environment or .env file."
        )
    kwargs = {"api_key": api_key}
    if BASE_URLS[provider]:
        kwargs["base_url"] = BASE_URLS[provider]
    return OpenAI(**kwargs)


def call_llm(messages, provider="openai"):
    """Send a chat completion request and return the response text."""
    if provider not in MODELS:
        raise ProviderError(f"Unknown provider '{provider}'. Use 'openai' or 'groq'.")

    client = _get_client(provider)

    try:
        resp = client.chat.completions.create(
            model=MODELS[provider],
            messages=messages,
            temperature=0.3,
            max_tokens=4096,
        )
    except Exception as exc:
        raise ProviderError(f"API request failed: {exc}") from exc

    return resp.choices[0].message.content
