"""
Crown of Kaliyug — Voiceover Agent (A-07)
Phase 3 · agents/audio_prod/voiceover/agent.py
"""
import json
from pathlib import Path
from loguru import logger
from .batch_generator import generate_batch_edge
from orchestrator.state_schema import EpisodeProductionState

OUTPUT_BASE = Path("output/audio")

def run(state: EpisodeProductionState) -> EpisodeProductionState:
    episode_id = state["episode_id"]
    script_path = state.get("script_draft_path") or state.get("script_locked_path", "")

    logger.info(f"[A-07] Voiceover Agent starting for {episode_id}")

    if not script_path or not Path(script_path).exists():
        logger.error(f"[A-07] Script path not found: {script_path}")
        return state

    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)

    out_dir = OUTPUT_BASE / episode_id / "voiceover"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect all lines
    lines = []
    for scene in script.get("scenes", []):
        if scene.get("is_tag_sequence"): continue
        for slot in scene.get("dialogue_slots", []):
            if slot.get("text"):
                lines.append(slot)

    success_count = generate_batch_edge(lines, out_dir)

    state["voiceover_ready"] = True
    state["audio_package_folder"] = str(OUTPUT_BASE / episode_id)
    logger.success(f"[A-07] {success_count} lines generated for {episode_id}")
    return state
