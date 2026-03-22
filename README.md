# Clean Code Bot

CLI tool that refactors Python files using an LLM. Feed it a messy script, get back a cleaned-up version with SOLID principles applied and docstrings added.

## What it does

- Takes a Python file as input, writes the refactored version to a new file
- Uses **Chain of Thought (CoT) prompting** — the model first analyses the code for problems (SOLID violations, code smells, missing docs), then refactors. This is implemented in `clean_code_bot/prompts.py`
- **Input sanitization** against prompt injection — validates syntax via `ast.parse`, scans for known injection patterns (role reassignment, fake system messages, etc.), and strips suspicious lines before they reach the model. See `clean_code_bot/sanitize.py`
- Supports **OpenAI** (`gpt-4o-mini`) and **Groq** (`llama-3.3-70b-versatile`, free tier available). Both use the same OpenAI-compatible API — switching is just a `-p` flag
- CLI built with `argparse`
- `examples/` folder with before/after samples (`dirty_calculator.py` → `clean_calculator.py`, `dirty_task_manager.py` → `clean_task_manager.py`)

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
