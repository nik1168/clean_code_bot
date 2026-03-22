import argparse
import sys

from dotenv import load_dotenv

from .engine import refactor_file
from .sanitize import ValidationError
from .providers import ProviderError


def _build_parser():
    p = argparse.ArgumentParser(
        prog="clean-code-bot",
        description="Refactor a Python file using an LLM — applies SOLID "
                    "principles, adds docstrings, and cleans up code smells.",
    )
    p.add_argument("input_file", help="path to the Python file to refactor")
    p.add_argument(
        "-o", "--output", default=None,
        help="output file path (default: clean_<filename>.py)",
    )
    p.add_argument(
        "-p", "--provider", choices=["openai", "groq"], default="openai",
        help="which LLM provider to use (default: openai)",
    )
    return p


def main(argv=None):
    load_dotenv()

    args = _build_parser().parse_args(argv)

    print(f"[clean-code-bot] Reading {args.input_file} ...")

    try:
        out, warnings = refactor_file(
            args.input_file,
            output_path=args.output,
            provider=args.provider,
        )
    except (FileNotFoundError, ValidationError, ProviderError) as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    if warnings:
        print("[clean-code-bot] Sanitizer warnings:")
        for w in warnings:
            print(f"  - possible prompt injection ({w})")

    print(f"[clean-code-bot] Done -> {out}")
