"""
Crown of Kaliyug — Sound Design Agent (A-09)
Phase 3 · agents/audio_prod/sfx/agent.py
"""
import json
from pathlib import Path
from loguru import logger
from .tag_extractor import extract_timeline
from orchestrator.state_schema import EpisodeProductionState

OUTPUT_BASE = Path("output/audio")

def run(state: EpisodeProductionState) -> EpisodeProductionState:
    episode_id = state["episode_id"]
    script_path = state.get("script_draft_path") or state.get("script_locked_path", "")

    logger.info(f"[A-09] Sound Design Agent starting for {episode_id}")

    if not script_path or not Path(script_path).exists():
        logger.error(f"[A-09] Script path not found: {script_path}")
        return state

    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)

    out_dir = OUTPUT_BASE / episode_id / "sfx"
    out_dir.mkdir(parents=True, exist_ok=True)

    for scene in script.get("scenes", []):
        scene_id = scene.get("scene_id", "")
        action = scene.get("action_lines", [])
        sfx_tags = scene.get("sfx_tags", [])
        location = scene.get("location", "")

        timeline = extract_timeline(scene_id, action, sfx_tags, location)
        
        out_path = out_dir / f"{scene_id}_sfx_timeline.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(timeline, f, indent=2, ensure_ascii=False)

    state["sfx_ready"] = True
    logger.success(f"[A-09] SFX design complete for {episode_id}")
    return state
