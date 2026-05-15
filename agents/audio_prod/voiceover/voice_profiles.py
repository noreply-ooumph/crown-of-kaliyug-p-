"""
Crown of Kaliyug - Voice Profiles
A-07 - agents/audio_prod/voiceover/voice_profiles.py
Loads and manages per-character voice settings.
"""
import yaml
from functools import lru_cache
from loguru import logger


@lru_cache(maxsize=1)
def load_profiles() -> dict:
    try:
        with open("config/voice_profiles.yaml") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load voice profiles: {e}")
        return {}


def get_character_profile(character_id: str) -> dict:
    profiles = load_profiles()
    return profiles.get("characters", {}).get(character_id, {
        "gtts_lang": "hi",
        "gtts_slow": False,
        "edge_voice": "hi-IN-MadhurNeural",
        "elevenlabs_voice_id": "",
    })


def get_edge_voice(character_id: str) -> str:
    profile = get_character_profile(character_id)
    return profile.get("edge_voice", "hi-IN-MadhurNeural")


def get_elevenlabs_voice_id(character_id: str) -> str:
    profile = get_character_profile(character_id)
    return profile.get("elevenlabs_voice_id", "")


def get_all_characters() -> list:
    profiles = load_profiles()
    return list(profiles.get("characters", {}).keys())
