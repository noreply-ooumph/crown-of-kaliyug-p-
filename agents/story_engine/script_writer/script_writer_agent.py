import json
from pathlib import Path
from loguru import logger
from database.db import get_db
from database.models import Episode
from agents.story_engine.script_writer.scene_generator import generate_script
from agents.story_engine.script_writer.teaser_cutter import generate_teasers
from orchestrator.state_schema import EpisodeProductionState

OUTPUT_DIR = Path("output/scripts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run(state: EpisodeProductionState) -> EpisodeProductionState:
    episode_id = state["episode_id"]
    season     = state.get("season", 1)
    retry      = state.get("script_retry_count", 0)

    logger.info(f"[A-02] Script Writer - {episode_id} (attempt {retry + 1})")

    with get_db() as db:
        ep = db.query(Episode).filter_by(id=episode_id).first()
        if not ep:
            state["errors"].append(f"Episode {episode_id} not in DB")
            return state
        outline = {
            "title_english":  ep.title_english,
            "title_hindi":    ep.title_hindi,
            "synopsis":       ep.synopsis,
            "key_events":     ep.key_events or [],
            "tone_reference": ep.parvas_covered,
            "runtime_target": ep.runtime_target,
        }

    retry_ctx = ""
    if retry > 0 and state.get("canon_result"):
        violations = state["canon_result"].get("violations", [])
        retry_ctx = "\n".join(
            f"- [{v['severity']}] {v.get('scene_id','')}: {v['issue']}"
            for v in violations
        )

    script  = generate_script(episode_id, outline, season, retry_ctx)
    teasers = generate_teasers(script, episode_id)
    script["teasers"] = teasers

    # Save JSON (for downstream agents)
    json_path = OUTPUT_DIR / f"{episode_id}_draft_{retry + 1}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    # Save TXT (for human reading)
    txt_path = OUTPUT_DIR / f"{episode_id}_draft_{retry + 1}.txt"
    _export_to_txt(script, txt_path)

    state["script_draft_path"]  = str(json_path)
    state["script_retry_count"] = retry + 1
    logger.success(f"[A-02] Script saved -> {txt_path} (and JSON for agents)")
    return state

def _export_to_txt(script, path):
    lines = []
    lines.append(f"EPISODE: {script.get('episode_id')}")
    lines.append(f"TITLE: {script.get('title_english')}")
    lines.append("=" * 60)
    for s in script.get("scenes", []):
        lines.append(f"\nSCENE {s.get('scene_id')}: {s.get('location')} ({s.get('interior_exterior')}) - {s.get('time_of_day')}")
        lines.append(f"CHARACTERS: {', '.join(s.get('characters_present', []))}")
        lines.append("-" * 40)
        lines.append("ACTION:")
        for action in s.get("action_lines", []):
            lines.append(f"  {action}")
        lines.append("\nDIALOGUE:")
        for d in s.get("dialogue_slots", []):
            char = d.get('character', 'UNKNOWN').upper()
            emotion = d.get('emotion_tag') or d.get('emotion_hint', 'formal')
            text = d.get('text') or f"<{d.get('context')}>"
            lines.append(f"  {char} {emotion}: {text}")
        lines.append("\n" + "." * 60)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))