"""
Crown of Kaliyug — Music Composer Agent (A-08)
Phase 3 · agents/audio_prod/music/agent.py
"""
import json
from pathlib import Path
from loguru import logger
from .theme_matcher import match, get_kurukshetra_fragment
from orchestrator.state_schema import EpisodeProductionState

OUTPUT_BASE = Path("output/audio")

def run(state: EpisodeProductionState) -> EpisodeProductionState:
    episode_id = state["episode_id"]
    season = state.get("season", 1)
    script_path = state.get("script_draft_path") or state.get("script_locked_path", "")

    logger.info(f"[A-08] Music Composer starting for {episode_id}")

    if not script_path or not Path(script_path).exists():
        logger.error(f"[A-08] Script path not found: {script_path}")
        return state

    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)

    out_dir = OUTPUT_BASE / episode_id / "music"
    out_dir.mkdir(parents=True, exist_ok=True)

    for scene in script.get("scenes", []):
        scene_id = scene.get("scene_id", "")
        location = scene.get("location", "")
        mood = scene.get("mood", "")

        theme = match(location, mood, season, scene_id)
        
        # Output prompt file
        out_path = out_dir / f"{scene_id}_music_prompt.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"THEME: {theme.get('name')}\n")
            f.write(f"PROMPT: {theme.get('suno_prompt')}\n")
            f.write(f"INSTRUMENTS: {theme.get('instruments', [])}\n")

    state["music_ready"] = True
    logger.success(f"[A-08] Music plan complete for {episode_id}")
    return state
