# Clean Code Bot

CLI tool that refactors Python files using an LLM. Feed it a messy script, get back a cleaned-up version with SOLID principles applied and docstrings added.

## What it does

- Takes a Python file as input, writes the refactored version to a new file
- Uses **Chain of Thought (CoT) prompting** — the model first analyses the code for problems (SOLID violations, code smells, missing docs), then refactors. This is implemented in `clean_code_bot/prompts.py`
- **Input sanitization** against prompt injection — validates syntax via `ast.parse`, scans for known injection patterns (role reassignment, fake system messages, etc.), and strips suspicious lines before they reach the model. See `clean_code_bot/sanitize.py`
- Supports **OpenAI** (`gpt-4o-mini`) and **Groq** (`llama-3.3-70b-versatile`, free tier available). Both use the same OpenAI-compatible API — switching is just a `-p` flag
- CLI built with `argparse`
- `examples/` folder with before/after samples (`dirty_calculator.py` → `clean_calculator.py`, `dirty_task_manager.py` → `clean_task_manager.py`)

## Demo

https://drive.google.com/file/d/1pCZcC_xcWAiGQZMAVkeCf5ioTnNOPyZZ/view?usp=sharing

## Setup

```bash
git clone https://github.com/nik1168/clean_code_bot.git
cd clean_code_bot
pip install -r requirements.txt
```

Set your API key — either as an env var or in a `.env` file (gitignored):

```bash
export OPENAI_API_KEY=sk-...
# or
export GROQ_API_KEY=gsk_...
```

Keys: [OpenAI](https://platform.openai.com/api-keys) (~$5 credit) | [Groq](https://console.groq.com) (free)

## Usage

```bash
python main.py examples/dirty_calculator.py                # output: examples/clean_dirty_calculator.py
python main.py examples/dirty_task_manager.py -p groq      # use groq instead
python main.py some_file.py -o cleaned.py                  # custom output path
```

## Where each requirement is implemented

| Requirement | Where in the code |
|---|---|
| Python development environment | `requirements.txt` — deps are `openai` and `python-dotenv`, install with `pip install -r requirements.txt` |
| Chain of Thought (CoT) prompting | `clean_code_bot/prompts.py`, lines 17-23 — comment block explains the technique. The prompt template (steps 1-4) forces the model to analyse smells, SOLID violations, and missing docs *before* writing any refactored code |
| Prompt Injection defense | `clean_code_bot/sanitize.py` — `validate_python_syntax()` confirms the input is real Python via `ast.parse`, `scan_for_injections()` checks against known attack patterns, `strip_injection_lines()` removes suspicious lines before they reach the model |
| LLM access (OpenAI + Groq) | `clean_code_bot/providers.py` — `call_llm()` handles both providers through the same OpenAI-compatible SDK, just swapping the base URL and model. Provider is selected via the `-p` CLI flag |
| CLI with argparse | `clean_code_bot/cli.py` — `_build_parser()` defines the interface (`input_file`, `-o`, `-p`), `main()` is the entry point |
| Pipeline orchestration | `clean_code_bot/engine.py` — `refactor_file()` runs the full pipeline: read file → sanitize → build prompt → call LLM → extract code from response → write output |
| Before/after examples | `examples/` folder — `dirty_calculator.py` / `clean_calculator.py` and `dirty_task_manager.py` / `clean_task_manager.py` |
| requirements.txt | Project root — lists `openai>=1.14.0` and `python-dotenv>=1.0.0` |

## Project structure

```
main.py                     # entry point
clean_code_bot/
  cli.py                    # argparse CLI
  engine.py                 # pipeline: sanitize → prompt → LLM → extract → write
  prompts.py                # CoT prompt templates
  providers.py              # OpenAI / Groq abstraction
  sanitize.py               # input validation + prompt injection defense
examples/
  dirty_calculator.py       # before
  clean_calculator.py       # after
  dirty_task_manager.py     # before
  clean_task_manager.py     # after
```
