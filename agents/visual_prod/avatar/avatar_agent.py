"""
Crown of Kaliyug — Avatar Agent (A-05)
Phase 2 · agents/visual_prod/avatar/avatar_agent.py

Maps characters to their avatar PNG files.
Avatars from: assets/avatars/
"""
import os
import json
from pathlib import Path
from loguru import logger

AVATAR_DIR = Path("assets/avatars")

# Character → avatar file mapping
AVATAR_MAP = {
    "yudhishthira": "yudhishthira_avatar.png",
    "bhima":        "bhima_avatar.png",
    "arjuna":       "arjuna_avatar.png",
    "nakula":       "nakula_avatar.png",
    "sahadeva":     "sahadeva_avatar.png",
    "dushasana":    "dushasana_avatar.png",
    "karna":        "karna_avatar.png",
    "shakuni":      "shakuni_avatar.png",
    "krishna":      "krishna_avatar.png",
    "draupadi":     "draupadi_avatar.png",
    "kunti":        "kunti_avatar.png",
    "gandhari":     "gandhari_avatar.png",
    "bhishma":      "bhishma_avatar.png",
    "drona":        "drona_avatar.png",
    "vidura":       "vidura_avatar.png",
    "dhritarashtra":"dhritarashtra_avatar.png",
    "abhimanyu":    "abhimanyu_avatar.png",
    "ghatotkacha":  "ghatotkacha_avatar.png",
    "ashwatthama":  "ashwatthama_avatar.png",
    "kripacharya":  "kripacharya_avatar.png",
    "balarama":     "balarama_avatar.png",
    "subhadra":     "subhadra_avatar.png",
    "hidimba":      "hidimba_avatar.png",
    # Fallbacks
    "duryodhana":   "dushasana_avatar.png",
}


def run(state: dict) -> dict:
    episode_id = state["episode_id"]
    logger.info(f"[A-05] Avatar Agent — {episode_id}")

    script_path = state.get("script_draft_path") or state.get("script_locked_path", "")
    try:
        import json as j
        with open(script_path, encoding="utf-8") as f:
            script = j.load(f)
    except Exception as e:
        logger.error(f"[A-05] Script load failed: {e}")
        state["errors"] = state.get("errors", []) + [str(e)]
        return state

    # Build scene → avatar mapping
    scene_avatars = {}
    for scene in script.get("scenes", []):
        scene_id   = scene.get("scene_id", "")
        characters = scene.get("characters_present", [])
        if not characters:
            characters = list(set(
                slot.get("character", "")
                for slot in scene.get("dialogue_slots", [])
                if slot.get("character")
            ))
        avatars    = {}
        for char in characters:
            char_lower = char.lower()
            avatar_file = AVATAR_MAP.get(char_lower, "")
            avatar_path = str(AVATAR_DIR / avatar_file) if avatar_file else ""
            if avatar_path and os.path.exists(avatar_path):
                avatars[char_lower] = avatar_path
            else:
                logger.warning(f"[A-05] No avatar for {char} in {scene_id}")
                avatars[char_lower] = ""
        scene_avatars[scene_id] = avatars

    state["scene_avatars"]  = scene_avatars
    state["avatar_ready"]   = True
    total = sum(1 for av in scene_avatars.values() for p in av.values() if p)
    logger.success(f"[A-05] {total} avatar paths mapped for {episode_id}")
    return state


def get_avatar(character: str) -> str:
    """Returns avatar path for a character. Empty string if not found."""
    avatar_file = AVATAR_MAP.get(character.lower(), "")
    if not avatar_file:
        return ""
    path = str(AVATAR_DIR / avatar_file)
    return path if os.path.exists(path) else ""


def get_scene_primary_avatar(characters: list) -> str:
    """Returns the most prominent character avatar for a scene."""
    priority = ["karna","draupadi","krishna","duryodhana","arjuna",
                "bhishma","shakuni","yudhishthira","kunti"]
    for char in priority:
        if char in [c.lower() for c in characters]:
            path = get_avatar(char)
            if path:
                return path
    for char in characters:
        path = get_avatar(char)
        if path:
            return path
    return ""
