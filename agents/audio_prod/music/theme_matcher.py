"""
Crown of Kaliyug - Theme Matcher
A-08 - agents/audio_prod/music/theme_matcher.py
Matches scenes to Series Bible music themes.
"""
import yaml
from functools import lru_cache
from loguru import logger


@lru_cache(maxsize=1)
def load_themes() -> dict:
    try:
        with open("config/music_themes.yaml") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load music themes: {e}")
        return {}


def match(location: str, mood: str, season: int, scene_id: str) -> dict:
    """
    Returns the correct music theme for a scene.
    Enforces all Series Bible music rules.
    """
    themes = load_themes().get("themes", {})
    loc    = location.lower()
    moo    = mood.lower()
    sc     = scene_id.lower()

    # HARDCODED - Abhimanyu death (S4E13) = single sarangi only
    if "abhimanyu" in sc or "chakravyuha" in loc:
        return themes.get("abhimanyu_death", {})

    # Battle scenes only from S4
    if season >= 4 and ("battle" in moo or "kurukshetra" in loc or "war" in loc):
        return themes.get("battle", {})

    # Nation-specific themes
    if any(k in loc for k in ["dwarka", "krishna"]):
        return themes.get("dwarka", {})

    if any(k in loc for k in ["panchala", "kampilya", "draupadi"]):
        return themes.get("panchala", {})

    # Default: Kuru Court
    return themes.get("kuru_court", {})


def get_kurukshetra_fragment(season: int) -> dict:
    """
    Returns Kurukshetra theme variant based on season.
    S1: fragmented barely-audible version.
    S4+: full theme.
    """
    themes = load_themes().get("themes", {})
    theme  = themes.get("kurukshetra_theme", {}).copy()
    if season < 4:
        theme["suno_prompt"] = (
            "Single barely-audible string fragment, hidden in the mix, "
            "incomplete melody, distant and haunting"
        )
        theme["name"] = "Kurukshetra Theme (Fragment - S1)"
    else:
        theme["name"] = "Kurukshetra Theme (Full - S4+)"
    return theme
