# settings.py
import json

SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'music_volume': 0.5, 'sfx_volume': 0.5}

def save_settings(music_volume, sfx_volume):
    settings = {'music_volume': music_volume, 'sfx_volume': sfx_volume}
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

settings = load_settings()
music_volume = settings['music_volume']
sfx_volume = settings['sfx_volume']
