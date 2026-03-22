import ast
import re

MAX_FILE_SIZE = 50_000  # bytes, roughly 50 KB

# Known prompt injection patterns — (regex, short label).
# Not exhaustive, but catches the most common tricks.
_INJECTION_PATTERNS = [
    (re.compile(r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts)", re.I),
     "instruction override"),
    (re.compile(r"you\s+are\s+now\s+", re.I), "role reassignment"),
    (re.compile(r"system\s*:\s*", re.I), "fake system message"),
    (re.compile(r"<\|?\s*system\s*\|?>", re.I), "system token injection"),
    (re.compile(r"act\s+as\s+(a|an|if)\s+", re.I), "role play injection"),
    (re.compile(r"do\s+not\s+refactor", re.I), "refusal command"),
]


class ValidationError(Exception):
    pass


def validate_file_size(source):
    if len(source.encode("utf-8")) > MAX_FILE_SIZE:
        raise ValidationError(
            f"File exceeds the {MAX_FILE_SIZE // 1000} KB limit. "
            "Split it into smaller modules first."
        )


def validate_python_syntax(source):
    """Make sure the input is actually parseable Python."""
    try:
        ast.parse(source)
    except SyntaxError as exc:
        raise ValidationError(
            f"Input is not valid Python (line {exc.lineno}): {exc.msg}"
        ) from exc


def scan_for_injections(source):
    """Check for lines that look like prompt injection attempts.

    We don't block outright because some patterns can appear in legit
    string literals — instead we flag them and strip them before sending
    to the model.
    """
    found = []
    for pattern, label in _INJECTION_PATTERNS:
        if pattern.search(source):
            found.append(label)
    return found


def strip_injection_lines(source):
    """Remove lines that match injection patterns from the source."""
    clean = []
    for line in source.splitlines():
        skip = False
        for pattern, _ in _INJECTION_PATTERNS:
            # only strip if the match is the main content of the line,
            # not buried deep inside a long string
            stripped = line.strip().strip("#").strip("\"'").strip()
            if pattern.search(stripped) and len(stripped) < 200:
                skip = True
                break
        if not skip:
            clean.append(line)
    return "\n".join(clean)


def sanitize(source):
    """Run all checks. Returns (cleaned_source, warnings).

    Raises ValidationError if the file can't be processed at all.
    """
    validate_file_size(source)
    validate_python_syntax(source)

    warnings = scan_for_injections(source)
    cleaned = strip_injection_lines(source) if warnings else source

    return cleaned, warnings
