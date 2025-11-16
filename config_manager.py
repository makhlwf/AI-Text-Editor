import json
import os

CONFIG_FILE = os.path.join(os.getenv("APPDATA"), "AITextEditor", "config.json")


def get_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "api_key": "",
            "shortcut": "ctrl+alt+x",
            "model": "gemini-2.5-flash-lite",
        }
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        if "model" not in config:
            config["model"] = "gemini-2.5-flash-lite"
        return config


def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
