import re
from pathlib import Path

from .sanitize import sanitize
from .prompts import build_refactor_prompt
from .providers import call_llm

_CODE_FENCE_RE = re.compile(r"```python\s*\n(.*?)```", re.DOTALL)


def _extract_code(response_text):
    """Pull the refactored source out of the model's markdown response.

    Grabs the *last* fenced python block — the model sometimes includes
    small snippets in its analysis before the full file at the end.
    """
    matches = _CODE_FENCE_RE.findall(response_text)
    if not matches:
        # nothing fenced — just return the raw response, user can sort it out
        return response_text.strip()
    return matches[-1].strip()


def _default_output(input_path):
    return input_path.parent / f"clean_{input_path.name}"


def refactor_file(input_path, output_path=None, provider="openai"):
    """Main pipeline: read file -> sanitize -> prompt LLM -> write output.

    Returns (output_path, list_of_warnings).
    """
    src = Path(input_path)
    if not src.is_file():
        raise FileNotFoundError(f"No such file: {src}")

    raw = src.read_text(encoding="utf-8")

    cleaned, warnings = sanitize(raw)

    messages = build_refactor_prompt(cleaned)
    response = call_llm(messages, provider=provider)

    refactored = _extract_code(response)

    dst = Path(output_path) if output_path else _default_output(src)
    dst.write_text(refactored + "\n", encoding="utf-8")

    return dst, warnings
