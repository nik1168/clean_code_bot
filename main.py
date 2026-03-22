#!/usr/bin/env python3
"""
Clean Code Bot — refactor Python files via LLM.

Usage:
    python main.py <file> [-o output] [-p openai|groq]

Examples:
    python main.py examples/dirty_calculator.py
    python main.py examples/dirty_calculator.py -p groq
    python main.py my_code.py -o refactored.py
"""
from clean_code_bot.cli import main

if __name__ == "__main__":
    main()
