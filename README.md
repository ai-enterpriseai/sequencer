

```
python -m sequencer sequence.md
```

```
# Run with specific models
python -m sequencer sequence.md -m "claude-3-5-sonnet-20240620" "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"

# Run multiple times
python -m sequencer sequence.md -n 3

# Specify output directory
python -m sequencer sequence.md -o ./my_results

# All options combined
python -m sequencer sequence.md -m "claude-3-5-sonnet-20240620" "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" -n 3 -o ./my_results

```


---

# Sequencer

Run prompt sequences for complex tasks.

## Installation

```bash
pip install sequencer
```

## Configuration

Create a `.env` file in your project directory:

```env
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
TOGETHER_API_KEY=your-key-here
HF_API_KEY=your-key-here
CEREBRAS_API_KEY=your-key-here
SAMBANOVA_API_KEY=your-key-here
```

## Creating Sequences

Create a markdown file with your sequence. The first section becomes the system prompt:

```markdown
# System Prompt
```
You are a helpful assistant.
```

---
# First Prompt
```
What is artificial intelligence?
```
```

## Usage

Basic:
```bash
sequencer sequence.md
```

With options:
```bash
sequencer sequence.md \
    -m "claude-3-5-sonnet-20240620" "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" \
    -n 3 \
    -o ./results
```

Options:
- `-m, --models`: Models to use
- `-n, --num-runs`: Number of runs (default: 1)
- `-o, --output-dir`: Output directory (default: ./results)

## Development

1. Clone the repository
2. Install dev dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`

