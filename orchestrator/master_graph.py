"""
Crown of Kaliyug — Master Orchestrator
Phase 0: Foundation
"""
from typing import Literal, List, Union
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from orchestrator.state_schema import EpisodeProductionState
from loguru import logger

# ── NODE FUNCTIONS (Placeholders) ──────────────────────────────────────────

def node_story_engine(state: EpisodeProductionState):
    logger.info(f"--- STORY ENGINE: Generating script for {state['episode_id']} ---")
    return {"script_raw": "Draft script content...", "status": "story_complete"}

def node_canon_guardian(state: EpisodeProductionState):
    logger.info(f"--- CANON GUARDIAN: Verifying canon integrity ---")
    return {"is_canon_safe": True, "canon_violations": []}

def node_shristi_approval(state: EpisodeProductionState):
    logger.info(f"--- SHRISTI HITL: Waiting for script approval ---")
    return {"script_approved": True, "shristi_approved": True}

def node_visual_production(state: EpisodeProductionState):
    logger.info(f"--- VISUAL PRODUCTION: Generating frames ---")
    return {"visual_assets": ["frame_01.png"], "vfx_status": "complete"}

def node_audio_production(state: EpisodeProductionState):
    logger.info(f"--- AUDIO PRODUCTION: Generating voice + music ---")
    return {"audio_assets": ["voice_01.mp3"], "audio_status": "complete"}

def node_post_production(state: EpisodeProductionState):
    logger.info(f"--- POST PRODUCTION: Final assembly ---")
    return {"video_s3_path": "s3://crown/final.mp4", "status": "completed"}

def node_analytics_engine(state: EpisodeProductionState):
    logger.info(f"--- ANALYTICS: Processing performance data ---")
    return {"metrics": {"views": 1000}, "status": "published", "published": True}

# ── CONDITIONAL LOGIC ──────────────────────────────────────────────────────

def should_continue_to_production(state: EpisodeProductionState) -> Union[str, List[str]]:
    if state.get("shristi_approved") and state.get("is_canon_safe"):
        return ["visual_prod", "audio_prod"]
    return "story_engine"

# ── GRAPH CONSTRUCTION ─────────────────────────────────────────────────────

def build_graph():
    workflow = StateGraph(EpisodeProductionState)

    # Add Nodes
    workflow.add_node("story_engine", node_story_engine)
    workflow.add_node("canon_guardian", node_canon_guardian)
    workflow.add_node("shristi_gate", node_shristi_approval)
    workflow.add_node("visual_prod", node_visual_production)
    workflow.add_node("audio_prod", node_audio_production)
    workflow.add_node("post_prod", node_post_production)
    workflow.add_node("analytics", node_analytics_engine)

    # Define Edges
    workflow.set_entry_point("story_engine")
    workflow.add_edge("story_engine", "canon_guardian")
    workflow.add_edge("canon_guardian", "shristi_gate")

    # In LangGraph, if returning a list from conditional edges, 
    # we can map labels to nodes. To avoid 'unhashable list' error,
    # we ensure the mapping is correct or omit it if returning node names directly.
    workflow.add_conditional_edges(
        "shristi_gate",
        should_continue_to_production,
        {
            "visual_prod": "visual_prod",
            "audio_prod": "audio_prod",
            "story_engine": "story_engine"
        }
    )

    workflow.add_edge("visual_prod", "post_prod")
    workflow.add_edge("audio_prod", "post_prod")
    workflow.add_edge("post_prod", "analytics")
    workflow.add_edge("analytics", END)

    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

# For module level access
app = build_graph()
