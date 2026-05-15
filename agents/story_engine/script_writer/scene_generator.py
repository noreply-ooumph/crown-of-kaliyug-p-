import json
from loguru import logger
from shared.llm.llm_client import call_llm_json
from agents.story_engine.script_writer.rag_retriever import retrieve_context

with open("prompts/script_writer_system.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def generate_script(episode_id, episode_outline, season, retry_context=""):
    characters = _extract_characters(episode_outline)
    bible_ctx = retrieve_context(episode_id, characters, season)
    system = f"{SYSTEM_PROMPT}\n\n{bible_ctx}"
    user_msg = f"""Generate script for {episode_id}.
Title: {episode_outline.get("title_english")}
Synopsis: {episode_outline.get("synopsis", "")}
Key Events: {json.dumps(episode_outline.get("key_events", []), ensure_ascii=False)}
Season: {season}"""
    if retry_context:
        user_msg += f"\nCANON FIXES:\n{retry_context}"
    logger.info(f"[A-02] Generating script for {episode_id}...")
    raw = call_llm_json(system_prompt=system, user_message=user_msg, max_tokens=8000)
    script = _normalize(raw, episode_id)
    logger.success(f"[A-02] {len(script.get('scenes', []))} scenes generated for {episode_id}")       
    return script

def _normalize(raw, episode_id):
    scenes = raw.get("scenes") or raw.get("script") or raw.get("screenplay") or []
    if not scenes:
        for val in raw.values():
            if isinstance(val, list) and len(val) > 0:
                scenes = val
                break
    normalized = []
    for i, s in enumerate(scenes, 1):
        action = s.get("action_lines") or s.get("action") or ([s["description"]] if s.get("description") else [])
        raw_dl = s.get("dialogue_slots") or s.get("dialogue") or []
        slots = []
        for j, d in enumerate(raw_dl, 1):
            slots.append({"slot_id": f"{episode_id}-SC{i:02d}-L{j:02d}", "character": d.get("character","").lower(), "delivery": "DIALOGUE", "context": d.get("line",""), "emotion_hint": "formal", "text": d.get("line",""), "emotion_tag": "[formal]"})
        normalized.append({"scene_id": s.get("scene_id") or f"{episode_id}-SC{i:02d}", "scene_number": s.get("scene_number") or s.get("scene") or i, "location": s.get("location",""), "interior_exterior": s.get("interior_exterior","EXT"), "time_of_day": s.get("time_of_day","DAY"), "characters_present": s.get("characters_present") or s.get("characters",[]), "mood": s.get("mood",""), "action_lines": action if isinstance(action, list) else [action], "dialogue_slots": slots, "vfx_required": s.get("vfx_required",[]), "sfx_tags": s.get("sfx_tags",[]), "is_tag_sequence": s.get("is_tag_sequence", False), "directors_note": s.get("directors_note","")})
    return {"episode_id": episode_id, "title_english": raw.get("title_english",""), "total_scenes": len(normalized), "estimated_runtime_min": 60, "scenes": normalized}

def _extract_characters(outline):
    text = " ".join(outline.get("key_events",[])).lower()
    full = ["yudhishthira","draupadi","karna","krishna","duryodhana","bhishma","shakuni","kunti","arjuna"]
    mapping = {"karna":["karna","anga"],"krishna":["krishna"],"draupadi":["draupadi"],"yudhishthira":["yudhishthira"],"duryodhana":["duryodhana"],"bhishma":["bhishma"],"shakuni":["shakuni","dice"],"kunti":["kunti"],"arjuna":["arjuna"]}
    found = [c for c,kws in mapping.items() if any(kw in text for kw in kws)]
    return found if found else full
