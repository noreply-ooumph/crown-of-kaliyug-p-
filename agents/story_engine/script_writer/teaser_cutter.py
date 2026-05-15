"""
Crown of Kaliyug — Teaser Cutter
Phase 1 · A-02 · agents/story_engine/script_writer/teaser_cutter.py
"""
import json
from loguru import logger
from shared.llm.llm_client import call_llm_json

SYSTEM = """You are a teaser editor for Crown of Kaliyug.
Select the most compelling scenes from a full episode script for 30s / 60s / 90s platform cuts.
Rules: Lead with drama. Prefer Karna or Draupadi scenes. Never spoil central revelation. End on cliffhanger.
Return ONLY valid JSON."""


def generate_teasers(full_script: dict, episode_id: str) -> dict:
    scenes = [
        {"scene_id": s["scene_id"], "location": s.get("location"),
         "characters": s.get("characters_present", []), "mood": s.get("mood"),
         "summary": (s.get("action_lines") or [""])[0][:150]}
        for s in full_script.get("scenes", [])
        if not s.get("is_tag_sequence")
    ]
    result = call_llm_json(
        system_prompt=SYSTEM,
        user_message=f"Episode: {episode_id}\nScenes:\n{json.dumps(scenes, indent=2)}\n\n"
                     "Return: {\"teaser_30s\":{\"scene_ids\":[...],\"rationale\":\"\"},"
                     "\"teaser_60s\":{...},\"teaser_90s\":{...}}",
        max_tokens=800,
    )
    logger.success(f"[A-02] Teasers generated for {episode_id}")
    return result