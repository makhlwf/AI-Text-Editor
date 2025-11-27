import json
import os

CONFIG_FILE = os.path.join(os.getenv("APPDATA"), "AITextEditor", "config.json")


def get_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "api_key": "",
            "shortcut": "ctrl+alt+x",
            "model": "gemini-1.5-flash-latest",
            "ai_provider": "gemini",
            "ollama_model": "gemma3",
        }
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        if "model" not in config:
            config["model"] = "gemini-1.5-flash-latest"
        if "ai_provider" not in config:
            config["ai_provider"] = "gemini"
        if "ollama_model" not in config:
            config["ollama_model"] = "gemma3"
        return config


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
