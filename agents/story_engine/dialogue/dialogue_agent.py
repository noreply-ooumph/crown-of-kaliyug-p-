import json
from pathlib import Path
from loguru import logger
from shared.llm.llm_client import call_llm_json
from agents.story_engine.dialogue.character_loader import load_character_prompt
from orchestrator.state_schema import EpisodeProductionState

def run(state: EpisodeProductionState) -> EpisodeProductionState:
    """
    A-03 Dialogue Agent entry point. Loads the script draft and fills dialogue slots.
    """
    draft_path = state.get("script_draft_path")
    if not draft_path or not Path(draft_path).exists():
        state["errors"].append(f"Script draft not found at {draft_path}")
        return state

    logger.info(f"[A-03] Dialogue Agent starting for {state['episode_id']}")

    # Load draft
    try:
        with open(draft_path, "r", encoding="utf-8") as f:
            script_data = json.load(f)
    except Exception as e:
        state["errors"].append(f"Failed to load script draft: {str(e)}")
        return state

    # Fill dialogue
    updated_script = fill_dialogue(script_data)

    # Save JSON back
    with open(draft_path, "w", encoding="utf-8") as f:
        json.dump(updated_script, f, ensure_ascii=False, indent=2)

    # Update TXT version
    txt_path = Path(draft_path).with_suffix(".txt")
    _export_to_txt(updated_script, txt_path)

    logger.success(f"[A-03] Dialogue filled and saved to {txt_path}")
    return state

def fill_dialogue(script_data):
    """
    Iterates through scenes and fills dialogue slots using character-specific prompts.
    """
    episode_id = script_data.get("episode_id", "UNKNOWN")
    
    for scene in script_data.get("scenes", []):
        scene_id = scene.get("scene_id")
        slots = scene.get("dialogue_slots", [])
        if not slots:
            continue
            
        logger.info(f"[A-03] Filling dialogue for {scene_id} ({len(slots)} slots)")
        
        for slot in slots:
            char_name = slot.get("character")
            if not char_name:
                continue
                
            try:
                system_prompt = load_character_prompt(char_name)
            except FileNotFoundError:
                logger.warning(f"[A-03] No prompt for {char_name}, using default.")
                system_prompt = f"You are {char_name.upper()}. Speak in the tone of 'Crown of Kaliyug'."

            user_msg = f"""SCENE CONTEXT:
Location: {scene.get('location')} {scene.get('time_of_day')}
Action: {" ".join(scene.get('action_lines', []))}
Other Characters: {", ".join(scene.get('characters_present', []))}

FILL THIS SLOT:
Slot ID: {slot.get('slot_id')}
Context/Intent: {slot.get('context')}
Emotion Hint: {slot.get('emotion_hint')}

Return the dialogue text and appropriate emotion tag from your instructions."""

            # Call LLM
            response = call_llm_json(system_prompt=system_prompt, user_message=user_msg)
            
            if isinstance(response, dict):
                if "lines" in response and isinstance(response["lines"], list) and len(response["lines"]) > 0:
                    line_data = response["lines"][0]
                    slot["text"] = line_data.get("text", slot.get("context", ""))
                    slot["emotion_tag"] = line_data.get("emotion_tag", f"[{slot.get('emotion_hint', 'formal')}]")
                else:
                    slot["text"] = response.get("text", slot.get("context", ""))
                    slot["emotion_tag"] = response.get("emotion_tag", f"[{slot.get('emotion_hint', 'formal')}]")
            
            logger.debug(f"[A-03] {char_name} ({scene_id}): {slot['text'][:30]}...")

    return script_data

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
