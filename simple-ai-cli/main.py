#!/usr/bin/env python3
"""
Simple AI CLI - A lightweight alternative to Claude Code
Features:
- Easy to install and use
- Support multiple AI models (OpenAI, Anthropic, Ollama, etc.)
- Customizable via config file
- Simple command-line interface
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Import optional dependencies
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class SimpleAIClient:
    """Simple AI client supporting multiple providers"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or Path.home() / ".simple-ai-cli" / "config.json"
        self.config = self.load_config()
        self.api_key = None
        self.model = None
        self.provider = None
        
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "provider": "openai",  # openai, anthropic, ollama
            "model": "gpt-3.5-turbo",
            "api_keys": {
                "openai": "",
                "anthropic": "",
            },
            "ollama_base_url": "http://localhost:11434",
            "temperature": 0.7,
            "max_tokens": 2048,
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    saved_config = json.load(f)
                    default_config.update(saved_config)
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
        
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"Configuration saved to {self.config_path}")
    
    def setup(self):
        """Interactive setup wizard"""
        print("=== Simple AI CLI Setup ===\n")
        
        # Choose provider
        print("Available providers:")
        print("1. OpenAI (GPT-3.5, GPT-4)")
        print("2. Anthropic (Claude)")
        print("3. Ollama (Local models)")
        
        choice = input("\nSelect provider (1-3) [default: 1]: ").strip() or "1"
        
        if choice == "1":
            self.config["provider"] = "openai"
            api_key = input("Enter your OpenAI API key: ").strip()
            self.config["api_keys"]["openai"] = api_key
            
            model = input("Enter model name [default: gpt-3.5-turbo]: ").strip() or "gpt-3.5-turbo"
            self.config["model"] = model
            
        elif choice == "2":
            self.config["provider"] = "anthropic"
            api_key = input("Enter your Anthropic API key: ").strip()
            self.config["api_keys"]["anthropic"] = api_key
            
            model = input("Enter model name [default: claude-3-haiku-20240307]: ").strip() or "claude-3-haiku-20240307"
            self.config["model"] = model
            
        elif choice == "3":
            self.config["provider"] = "ollama"
            base_url = input("Enter Ollama base URL [default: http://localhost:11434]: ").strip() or "http://localhost:11434"
            self.config["ollama_base_url"] = base_url
            
            model = input("Enter model name [default: llama2]: ").strip() or "llama2"
            self.config["model"] = model
        
        # Temperature
        temp = input("Enter temperature (0.0-2.0) [default: 0.7]: ").strip() or "0.7"
        self.config["temperature"] = float(temp)
        
        # Max tokens
        max_tokens = input("Enter max tokens [default: 2048]: ").strip() or "2048"
        self.config["max_tokens"] = int(max_tokens)
        
        self.save_config()
        print("\nSetup complete! You can now use the chat command.")
    
    def chat_openai(self, message):
        """Chat using OpenAI API"""
        if not HAS_OPENAI:
            print("Error: openai package not installed. Run: pip install openai")
            return None
        
        api_key = self.config["api_keys"].get("openai") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OpenAI API key not configured")
            return None
        
        client = OpenAI(api_key=api_key)
        
        try:
            response = client.chat.completions.create(
                model=self.config["model"],
                messages=[{"role": "user", "content": message}],
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def chat_anthropic(self, message):
        """Chat using Anthropic API"""
        api_key = self.config["api_keys"].get("anthropic") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: Anthropic API key not configured")
            return None
        
        if not HAS_REQUESTS:
            print("Error: requests package not installed. Run: pip install requests")
            return None
        
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.config["model"],
            "max_tokens": self.config["max_tokens"],
            "messages": [{"role": "user", "content": message}]
        }
        
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def chat_ollama(self, message):
        """Chat using Ollama (local models)"""
        if not HAS_REQUESTS:
            print("Error: requests package not installed. Run: pip install requests")
            return None
        
        base_url = self.config["ollama_base_url"].rstrip("/")
        
        data = {
            "model": self.config["model"],
            "prompt": message,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/generate",
                json=data
            )
            response.raise_for_status()
            result = response.json()
            return result["response"]
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def chat(self, message):
        """Send a chat message to the configured AI provider"""
        provider = self.config["provider"]
        
        if provider == "openai":
            return self.chat_openai(message)
        elif provider == "anthropic":
            return self.chat_anthropic(message)
        elif provider == "ollama":
            return self.chat_ollama(message)
        else:
            print(f"Error: Unknown provider '{provider}'")
            return None


def main():
    parser = argparse.ArgumentParser(
        description="Simple AI CLI - A lightweight alternative to Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s setup              # Run interactive setup
  %(prog)s chat "Hello!"      # Send a single message
  %(prog)s --model gpt-4 "Explain quantum computing"  # Use specific model
  %(prog)s config             # Show current configuration
        """
    )
    
    parser.add_argument("action", nargs="?", choices=["setup", "chat", "config"], 
                       help="Action to perform")
    parser.add_argument("message", nargs="?", help="Message to send (for chat action)")
    parser.add_argument("--model", "-m", help="Override model for this request")
    parser.add_argument("--provider", "-p", choices=["openai", "anthropic", "ollama"],
                       help="Override provider for this request")
    parser.add_argument("--config", "-c", help="Path to config file")
    
    args = parser.parse_args()
    
    client = SimpleAIClient(config_path=args.config)
    
    if args.action == "setup" or (args.action is None and not client.config_path.exists()):
        client.setup()
        return
    
    if args.action == "config":
        print("Current Configuration:")
        print(json.dumps(client.config, indent=2))
        return
    
    if args.action == "chat" or args.message:
        message = args.message
        if not message:
            # Read from stdin if no message provided
            message = sys.stdin.read().strip()
        
        if not message:
            print("Error: No message provided")
            print("Usage: simple-ai chat \"Your message here\"")
            return
        
        # Override config if specified
        if args.model:
            client.config["model"] = args.model
        if args.provider:
            client.config["provider"] = args.provider
        
        print(f"Thinking... (using {client.config['provider']}/{client.config['model']})")
        response = client.chat(message)
        
        if response:
            print("\n" + "="*50)
            print(response)
            print("="*50)


if __name__ == "__main__":
    main()
