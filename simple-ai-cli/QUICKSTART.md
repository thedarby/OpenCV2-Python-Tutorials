# Simple AI CLI - Quick Start Guide

## 🚀 Installation (30 seconds)

### Option 1: Automatic Install (Recommended)

```bash
cd simple-ai-cli
./run.sh
```

This will:
- Create a virtual environment
- Install required dependencies
- Show you next steps

### Option 2: Manual Install

```bash
cd simple-ai-cli
pip install -r requirements.txt
```

## ⚙️ Setup (1 minute)

Run the interactive setup:

```bash
python main.py setup
```

You'll be asked to:
1. Choose your AI provider:
   - **OpenAI** - GPT-3.5, GPT-4 (requires API key)
   - **Anthropic** - Claude models (requires API key)
   - **Ollama** - Local models (FREE, no API key needed!)

2. Enter your API key (if using OpenAI or Anthropic)
3. Choose your preferred model
4. Set temperature and max tokens

## 💬 Usage Examples

### Basic Chat

```bash
python main.py chat "Hello, how are you?"
```

### Use Different Models

```bash
# Use GPT-4 for this request
python main.py -m gpt-4 chat "Write a poem"

# Use Claude
python main.py -p anthropic chat "Explain quantum physics"

# Use local Ollama model
python main.py -p ollama -m llama2 chat "What is AI?"
```

### View Configuration

```bash
python main.py config
```

## 🎯 Quick Tips

### For OpenAI Users
1. Get your API key from: https://platform.openai.com/api-keys
2. Recommended models: `gpt-3.5-turbo` (fast/cheap), `gpt-4` (smart)

### For Anthropic Users
1. Get your API key from: https://console.anthropic.com/settings/keys
2. Recommended models: `claude-3-haiku-20240307` (fast), `claude-3-sonnet-20240229` (balanced)

### For Ollama Users (FREE!)
1. Install Ollama from: https://ollama.ai
2. Download a model: `ollama pull llama2`
3. No API key needed - runs locally on your computer!

## 🔧 Make It Even Easier

### Create a Shortcut (Linux/Mac)

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
alias ai='python /workspace/simple-ai-cli/main.py'
```

Then reload your shell:
```bash
source ~/.bashrc
```

Now you can use:
```bash
ai chat "Hello!"
ai -m gpt-4 chat "Complex question"
```

### Windows Users

Create a batch file `ai.bat`:
```batch
@echo off
python C:\path\to\simple-ai-cli\main.py %*
```

Put it in a folder in your PATH, then use:
```cmd
ai chat "Hello!"
```

## ❓ Troubleshooting

**Problem**: "Module not found"
- **Solution**: `pip install -r requirements.txt`

**Problem**: "API key not configured"
- **Solution**: Run `python main.py setup` again

**Problem**: Ollama connection failed
- **Solution**: Make sure Ollama is running: `ollama serve`

## 📝 What's Next?

You now have a simple, customizable AI CLI tool! 

- Try different models to see which you like
- Adjust temperature for more creative/responsive answers
- Use it in your scripts and workflows
- Modify the code to add your own features!

Happy coding! 🎉
