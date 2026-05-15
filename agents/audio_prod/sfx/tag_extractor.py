"""
Crown of Kaliyug - SFX Tag Extractor
A-09 - agents/audio_prod/sfx/tag_extractor.py
Extracts SFX timeline from scene action lines using LLM.
"""
from loguru import logger
from shared.llm.llm_client import call_llm_json

SYSTEM = """You are a sound designer for Crown of Kaliyug.
Extract a sound effects timeline from scene action lines.
Return ONLY JSON:
{
  "sfx_timeline": [
    {"timestamp_hint": "scene_start", "sfx_type": "crowd_murmur", "intensity": "low", "duration_sec": 10},
    {"timestamp_hint": "karna_enters", "sfx_type": "crowd_gasp", "intensity": "high", "duration_sec": 3}
  ],
  "ambient_layer": "hastinapur_court_day"
}"""


def extract_timeline(scene_id: str, action_lines: list,
                     sfx_tags: list, location: str) -> dict:
    action_text = " ".join(action_lines)[:400]
    try:
        return call_llm_json(
            system_prompt=SYSTEM,
            user_message=(
                f"Scene: {scene_id}\n"
                f"Location: {location}\n"
                f"Action: {action_text}\n"
                f"SFX tags: {sfx_tags}"
            ),
            max_tokens=500,
        )
    except Exception as e:
        logger.warning(f"SFX extraction failed for {scene_id}: {e}")
        return {
            "sfx_timeline": [],
            "ambient_layer": location.lower().replace(" ", "_")
        }
