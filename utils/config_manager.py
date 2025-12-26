import json
import os
import platform

# Default to standard, but allow override for testing
DEFAULT_PATH = "user_config.json"
CONFIG_FILE = os.getenv("RILEY_CONFIG_PATH", DEFAULT_PATH)

DEFAULT_CONFIG = {
    "user_name": "User",
    "ai_name": "Riley",
    "evolution_mode": "Static",
    "theme": "Dark",
    "first_run": True
}

def load_config():
    # Reload path in case env var changed at runtime
    current_path = os.getenv("RILEY_CONFIG_PATH", DEFAULT_PATH)
    if not os.path.exists(current_path):
        return DEFAULT_CONFIG
    try:
        with open(current_path, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(data):
    current_path = os.getenv("RILEY_CONFIG_PATH", DEFAULT_PATH)
    current = load_config()
    current.update(data)
    with open(current_path, "w") as f:
        json.dump(current, f, indent=4)
