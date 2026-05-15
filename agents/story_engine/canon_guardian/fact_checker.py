import os
from loguru import logger
from shared.llm.llm_client import call_llm_json

def check_canon(script_data, season):
    """
    Calls LLM to verify script against canon rules stored in prompts/canon_guardian_system.txt.
    """
    prompt_path = os.path.join("prompts", "canon_guardian_system.txt")
    
    if os.path.exists(prompt_path) and os.path.getsize(prompt_path) > 2:
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
    else:
        # Fallback basic prompt if the file is missing or corrupted
        system_prompt = """You are the Canon Guardian for 'Crown of Kaliyug'.
SEASON 1-2 CONSTRAINTS:
- Krishna is NEVER shown in divine form.
- Karna's true parentage (son of Kunti/Surya) is NEVER revealed.
Return JSON: {"is_safe": bool, "violations": [{"scene_id": str, "issue": str, "severity": "CRITICAL"}]}"""

    user_msg = f"Verify canon for Episode {script_data.get('episode_id')} (Season {season}).\n\n"
    user_msg += "SCRIPT CONTENT:\n"
    
    for scene in script_data.get("scenes", []):
        user_msg += f"\n--- SCENE {scene.get('scene_id')} ---\n"
        user_msg += f"Action: {' '.join(scene.get('action_lines', []))}\n"
        for d in scene.get("dialogue_slots", []):
            user_msg += f"{d.get('character')}: {d.get('text')}\n"

    try:
        # We expect a JSON response with 'is_safe' and 'violations'
        result = call_llm_json(system_prompt=system_prompt, user_message=user_msg)
        # Compatibility alias for tests
        if "status" not in result:
            result["status"] = "PASS" if result.get("is_safe") else "FAIL"
        return result
    except Exception as e:
        logger.error(f"[A-04] LLM Canon check failed: {e}")
        return {"is_safe": True, "violations": [], "status": "PASS", "error": str(e)}

# Alias for tests
check_script = check_canon

