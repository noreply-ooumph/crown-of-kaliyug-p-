"""
Crown of Kaliyug - SFX Library
A-09 - agents/audio_prod/sfx/sfx_library.py
Maps SFX types to catalog IDs and fetch logic.
"""
import json
import os
from loguru import logger


def load_catalog() -> dict:
    path = "assets/sfx_catalog.json"
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def lookup(sfx_type: str) -> dict:
    """Returns catalog entry for an SFX type if available."""
    catalog = load_catalog()
    return catalog.get(sfx_type, {})


def get_ambient_for_location(location: str) -> str:
    """Returns recommended ambient SFX type for a location."""
    loc = location.lower()
    mapping = {
        "hastinapur":    "iron_pillars_echo_crowd",
        "tournament":    "crowd_100k_breathing",
        "forest":        "forest_dawn_birds",
        "river":         "river_ghats_dawn_herons",
        "battlefield":   "distant_war_drums_wind",
        "court":         "court_murmur_footsteps",
        "chambers":      "oil_lamp_crackle_silence",
        "dwarka":        "ocean_coastal_wind_seagulls",
        "panchala":      "djembe_drums_distant_crowd",
        "gandhara":      "mountain_wind_stone_echo",
    }
    for key, val in mapping.items():
        if key in loc:
            return val
    return "generic_indoor_silence"
