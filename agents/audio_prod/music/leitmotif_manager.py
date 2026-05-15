"""
Crown of Kaliyug - Leitmotif Manager
A-08 - agents/audio_prod/music/leitmotif_manager.py
Manages character-specific musical motifs.
"""

# Character leitmotifs from Series Bible
LEITMOTIFS = {
    "karna": {
        "name": "Karna Leitmotif",
        "description": "War drums building slowly, never resolved. Stops before completion.",
        "suno_prompt": "War drums building slowly, unresolved tension, drums stop before climax",
        "emotion": "tragic dignity",
    },
    "draupadi": {
        "name": "Draupadi Leitmotif",
        "description": "Single unaccompanied female voice - no instruments, no harmony.",
        "suno_prompt": "Single female voice, no instruments, no harmony, raw and unaccompanied",
        "emotion": "fierce grief",
    },
    "krishna": {
        "name": "Krishna Leitmotif",
        "description": "Bansuri flute, coastal Dwarka rhythm. Goes silent before terrible events.",
        "suno_prompt": "Bansuri flute, coastal Indian rhythm, light and playful, ocean undertone",
        "emotion": "divine playfulness",
    },
    "bhishma": {
        "name": "Bhishma / Kuru Theme",
        "description": "Kuru Court theme in its most mournful register.",
        "suno_prompt": "Raga Bhairav in mournful register, slow and ancient, weight of centuries",
        "emotion": "ancient grief",
    },
    "shakuni": {
        "name": "Shakuni Leitmotif",
        "description": "Light, almost playful. A single dice click underneath.",
        "suno_prompt": "Light playful strings, single bone click underneath, deceptively warm",
        "emotion": "concealed vengeance",
    },
}


def get_character_leitmotif(character_id: str) -> dict:
    return LEITMOTIFS.get(character_id, {})


def get_scene_leitmotifs(characters_present: list) -> list:
    """Returns all relevant leitmotifs for characters in a scene."""
    return [
        {"character": c, "leitmotif": get_character_leitmotif(c)}
        for c in characters_present
        if get_character_leitmotif(c)
    ]
