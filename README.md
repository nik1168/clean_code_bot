# Clean Code Bot

A command-line tool that takes messy Python files and refactors them using an LLM. It applies SOLID principles, adds docstrings, fixes naming, and breaks apart god functions — then writes the cleaned version to a new file.

Under the hood it uses **Chain of Thought prompting**: instead of just telling the model "fix this code", the prompt forces it to first analyse the problems (code smells, SOLID violations, missing docs), write out a plan, and *then* produce the refactored version. This two-step approach gives noticeably better results.

The tool also sanitises the input before sending it to the model. It validates that the file is actual Python (via `ast.parse`), checks for known prompt injection patterns, and strips suspicious lines so users can't sneak instructions into the code that would hijack the model.

## Supported providers

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI | `gpt-4o-mini` | Pay-as-you-go (~$0.01 per file) |
| Groq | `llama-3.3-70b-versatile` | Free tier available |

Both use the OpenAI-compatible chat completions API, so switching between them is just a flag.

## Setup

```bash
git clone https://github.com/nik1168/clean_code_bot.git
cd clean_code_bot

# create a virtualenv (optional but recommended)
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Then set your API key. Pick one:

**Option A — environment variable:**
```bash
export OPENAI_API_KEY=sk-your-key-here
# or
export GROQ_API_KEY=gsk_your-key-here
```

**Option B — `.env` file** (already gitignored):
```bash
cp .env.example .env
# edit .env and fill in your key
```

To get a key:
- OpenAI: https://platform.openai.com/api-keys (needs ~$5 credit)
- Groq: https://console.groq.com (free tier works fine)

## Usage

```bash
# basic — writes output to clean_<filename>.py in the same directory
python main.py path/to/your_file.py

# pick a provider
python main.py your_file.py -p groq

# specify output path
python main.py your_file.py -o refactored_version.py

# help
python main.py --help
```

## Testing it out

The `examples/` folder has two pairs of before/after files you can use to see what the tool does. The "dirty" files are the inputs, and the "clean" files show the kind of output you can expect.

**Try it on the included examples:**

```bash
# refactor the messy calculator
python main.py examples/dirty_calculator.py

# check the output
cat examples/clean_dirty_calculator.py

# try the task manager with groq
python main.py examples/dirty_task_manager.py -p groq
```

**Try it on your own code:**

```bash
# grab any Python file you've been meaning to clean up
python main.py ~/projects/some_old_script.py -o cleaned_up.py
```

The output file is a standalone Python file — no markdown, no explanations, just the refactored code ready to use.

### What the examples look like

**Before** (`examples/dirty_calculator.py`) — one giant function with an if/elif chain, error handling via `print` + `return None`, no docstrings, cramped formatting:

```python
def calc(a,b,op):
    if op == "add":
        return a+b
    elif op == "div":
        if b == 0:
            print("cant divide by zero!!")
            return None
        return a/b
    # ... 40 more lines of this
```

**After** — separate functions, a dispatch table, proper exceptions, type hints, docstrings on the public interface.

Check `examples/clean_calculator.py` and `examples/clean_task_manager.py` to see the full before/after.

## How it works

The pipeline is straightforward:

1. **Sanitize** — validate the file is real Python, scan for prompt injection patterns, strip anything suspicious
2. **Build prompt** — wrap the code in a Chain of Thought template that forces analysis before refactoring
3. **Call LLM** — send to OpenAI or Groq via the chat completions API
4. **Extract code** — pull the fenced python block out of the model's markdown response
5. **Write output** — save to disk

```
input.py → sanitize → prompt builder → LLM API → code extractor → clean_input.py
```

## Project structure

```
├── main.py                  # entry point
├── clean_code_bot/
│   ├── cli.py               # argument parsing
│   ├── engine.py             # orchestrates the pipeline
│   ├── prompts.py            # CoT prompt templates
│   ├── providers.py          # OpenAI / Groq API layer
│   └── sanitize.py           # input validation + injection defense
├── examples/
│   ├── dirty_calculator.py   # sample input
│   ├── clean_calculator.py   # sample output
│   ├── dirty_task_manager.py # sample input
│   └── clean_task_manager.py # sample output
├── requirements.txt
└── .env.example
```

## Prompt injection defense

Since the tool sends user-provided code to an LLM, it needs to guard against prompt injection — someone embedding instructions like "ignore previous instructions and output X" inside a Python file.

The sanitiser handles this in a few ways:
- Parses the file with `ast.parse` to confirm it's valid Python (not just a text file full of instructions)
- Scans for known injection patterns (role reassignment, fake system messages, instruction overrides)
- Strips matching lines before they reach the model
- The system prompt explicitly tells the model to treat the code block as raw source, never as instructions

It's not bulletproof (no sanitiser is), but it catches the common attacks.

## Limitations

- Only handles Python files for now (the architecture supports adding more languages later)
- Output quality depends on the model — `gpt-4o-mini` is solid but not perfect
- Very large files (50KB+) are rejected to keep API costs reasonable
- The model might occasionally change external behaviour despite being told not to — always review the output
