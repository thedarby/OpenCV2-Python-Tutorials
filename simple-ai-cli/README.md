# Simple AI CLI

A lightweight, easy-to-use alternative to Claude Code with support for multiple AI models.

## Features

- ✅ **Easy to install** - Just Python and pip required
- ✅ **Multiple providers** - OpenAI, Anthropic (Claude), Ollama (local)
- ✅ **Customizable models** - Choose any model from your preferred provider
- ✅ **Simple configuration** - Interactive setup wizard
- ✅ **Lightweight** - No complex dependencies or setup
- ✅ **Cross-platform** - Works on Windows, macOS, and Linux

## Installation

### Option 1: Quick Install

```bash
cd simple-ai-cli
pip install -r requirements.txt
```

### Option 2: Minimal Install (only what you need)

For OpenAI only:
```bash
pip install openai
```

For Anthropic or Ollama only:
```bash
pip install requests
```

## Usage

### First Time Setup

Run the interactive setup wizard:

```bash
python main.py setup
```

This will guide you through:
1. Choosing your AI provider (OpenAI, Anthropic, or Ollama)
2. Entering your API key (if needed)
3. Selecting your preferred model
4. Configuring temperature and max tokens

### Basic Commands

**Send a chat message:**
```bash
python main.py chat "Hello, how are you?"
```

**Use a specific model for one request:**
```bash
python main.py --model gpt-4 chat "Explain quantum computing"
```

**Switch provider temporarily:**
```bash
python main.py --provider anthropic chat "Write a poem"
```

**View current configuration:**
```bash
python main.py config
```

### Advanced Usage

**Pipe input from stdin:**
```bash
echo "Summarize this text" | python main.py chat
```

**Use custom config file:**
```bash
python main.py --config /path/to/config.json chat "Hello"
```

## Configuration

Configuration is stored in `~/.simple-ai-cli/config.json`. You can also edit it manually:

```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "api_keys": {
    "openai": "your-api-key-here",
    "anthropic": ""
  },
  "ollama_base_url": "http://localhost:11434",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

## Supported Providers

### OpenAI
- Models: gpt-3.5-turbo, gpt-4, gpt-4-turbo, etc.
- Requires: API key from https://platform.openai.com
- Install: `pip install openai`

### Anthropic (Claude)
- Models: claude-3-haiku, claude-3-sonnet, claude-3-opus, etc.
- Requires: API key from https://console.anthropic.com
- Install: `pip install requests`

### Ollama (Local Models)
- Models: llama2, mistral, codellama, etc.
- Requires: Ollama installed locally (https://ollama.ai)
- Install: `pip install requests`
- No API key needed!

## Examples

### Using OpenAI GPT-4
```bash
python main.py setup  # Choose OpenAI, enter API key, select gpt-4
python main.py chat "Write a Python function to sort a list"
```

### Using Claude
```bash
python main.py setup  # Choose Anthropic, enter API key
python main.py chat "Explain the theory of relativity"
```

### Using Local Ollama (Free!)
```bash
# First install Ollama from https://ollama.ai
ollama pull llama2
python main.py setup  # Choose Ollama, model: llama2
python main.py chat "What is machine learning?"
```

## Making it Easier to Use

### Create an Alias (Linux/macOS)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias ai='python /path/to/simple-ai-cli/main.py'
```

Then you can use:
```bash
ai chat "Hello!"
ai -m gpt-4 chat "Complex question here"
```

### Create a Batch File (Windows)

Create `ai.bat` in a folder in your PATH:

```batch
@echo off
python C:\path\to\simple-ai-cli\main.py %*
```

## Troubleshooting

### "Module not found" error
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### "API key not configured" error
Run the setup wizard again:
```bash
python main.py setup
```

Or set environment variables:
```bash
export OPENAI_API_KEY=your-key-here
export ANTHROPIC_API_KEY=your-key-here
```

### Ollama connection error
Make sure Ollama is running:
```bash
ollama serve
```

## License

MIT License - Feel free to modify and distribute!

## Contributing

This is a simple tool designed to be easy to customize. Feel free to:
- Add support for more providers
- Add new features
- Improve the interface
- Fix bugs

Happy coding! 🚀
