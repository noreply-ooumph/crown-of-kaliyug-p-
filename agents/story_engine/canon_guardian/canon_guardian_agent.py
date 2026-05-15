import json
from pathlib import Path
from loguru import logger
from orchestrator.state_schema import EpisodeProductionState
from agents.story_engine.canon_guardian.fact_checker import check_canon

def run(state: EpisodeProductionState) -> EpisodeProductionState:
    """
    A-04 Canon Guardian entry point. Verifies script adherence to the series bible and canon rules.
    """
    script_path = state.get("script_draft_path")
    if not script_path or not Path(script_path).exists():
        state["errors"].append(f"Script draft not found for canon check at {script_path}")
        return state

    logger.info(f"[A-04] Canon Guardian verifying {state['episode_id']}")

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script_data = json.load(f)
    except Exception as e:
        state["errors"].append(f"Failed to load script for canon check: {str(e)}")
        return state

    # Perform canon check
    season = state.get("season", 1)
    canon_result = check_canon(script_data, season)
    
    state["canon_result"] = canon_result
    state["is_canon_safe"] = canon_result.get("is_safe", True)

    if not state["is_canon_safe"]:
        violations = canon_result.get("violations", [])
        logger.warning(f"[A-04] {len(violations)} Canon Violations Found in {state['episode_id']}!")
        for v in violations:
            logger.warning(f"  - [{v.get('severity')}] {v.get('scene_id')}: {v.get('issue')}")
    else:
        logger.success(f"[A-04] {state['episode_id']} passed canon check.")

    return state
