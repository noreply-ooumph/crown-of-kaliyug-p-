"""
Crown of Kaliyug — Episode Tag Enforcer
Phase 4 · agents/post_prod/editor/tag_enforcer.py

RULE (Series Bible — NON-OVERRIDABLE):
  is_tag_sequence = True  →  music ONLY, 8 minutes
                           →  ZERO voiceover
                           →  ZERO dialogue
                           →  Kurukshetra theme (fragmented in S1)

This rule cannot be bypassed by any agent or human input.
"""
from loguru import logger


def is_tag_scene(scene: dict) -> bool:
    return scene.get("is_tag_sequence", False)


def enforce_tag_rules(scene: dict, clip_config: dict) -> dict:
    """
    Enforces tag sequence rules on clip config.
    Returns modified config — voiceover suppressed, music-only mode.
    """
    if not is_tag_scene(scene):
        return clip_config

    logger.info(f"[TagEnforcer] {scene.get('scene_id')} — TAG SEQUENCE enforced")

    # Force music-only mode — non-overridable
    clip_config["voiceover_enabled"] = False
    clip_config["dialogue_enabled"]  = False
    clip_config["subtitle_enabled"]  = False
    clip_config["music_enabled"]     = True
    clip_config["music_volume_db"]   = -8    # full instrumental volume
    clip_config["target_duration"]   = 480   # 8 minutes = 480 seconds
    clip_config["tag_enforced"]      = True

    return clip_config


def validate_tag_clip(scene: dict, clip_config: dict) -> bool:
    """Validates that tag rules were properly applied."""
    if not is_tag_scene(scene):
        return True
    if clip_config.get("voiceover_enabled", True):
        logger.error(f"[TagEnforcer] VIOLATION: voiceover not suppressed in tag scene!")
        return False
    if not clip_config.get("tag_enforced"):
        logger.error(f"[TagEnforcer] VIOLATION: tag rules not enforced!")
        return False
    return True
