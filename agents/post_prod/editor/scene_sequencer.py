"""
Crown of Kaliyug — Scene Sequencer
Phase 4 · agents/post_prod/editor/scene_sequencer.py

Orders video clips per script scene_order.
S1E01: Cold Open → Act 1 Tournament → Act 2 Court → Act 3 → 8-min Tag
"""
import os
from pathlib import Path
from loguru import logger


def get_ordered_clips(episode_id: str, scenes: list) -> list:
    """
    Returns ordered list of clip info dicts based on script scene order.
    Each dict: {scene_id, video_path, is_tag, scene_number, location}
    """
    video_dir = Path("output/video") / episode_id
    ordered   = []

    for scene in sorted(scenes, key=lambda s: s.get("scene_number", 99)):
        scene_id  = scene.get("scene_id", "")
        is_tag    = scene.get("is_tag_sequence", False)
        video_path = str(video_dir / f"{scene_id}.mp4")

        ordered.append({
            "scene_id":     scene_id,
            "scene_number": scene.get("scene_number", 0),
            "video_path":   video_path,
            "video_exists": os.path.exists(video_path),
            "is_tag":       is_tag,
            "location":     scene.get("location", ""),
            "mood":         scene.get("mood", ""),
            "characters":   scene.get("characters_present", []),
        })

    ready   = sum(1 for c in ordered if c["video_exists"])
    pending = sum(1 for c in ordered if not c["video_exists"])
    logger.info(f"[Sequencer] {episode_id}: {ready} clips ready, {pending} pending A-06")
    return ordered


def validate_sequence(clips: list) -> bool:
    """Check all clips exist before assembly."""
    missing = [c["scene_id"] for c in clips if not c["video_exists"]]
    if missing:
        logger.warning(f"[Sequencer] Missing clips: {missing}")
        return False
    return True
