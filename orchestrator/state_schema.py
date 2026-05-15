"""
Crown of Kaliyug — Master State Schema
Phase 0: Foundation
"""
from typing import TypedDict, List, Optional, Annotated, Dict
import operator

class EpisodeProductionState(TypedDict):
    # Metadata
    episode_id: str
    season_id: int
    title_en: Optional[str]
    title_hi: Optional[str]
    
    # Story Phase
    script_raw: Optional[str]
    script_final: Optional[str]
    script_draft_path: Optional[str]
    script_locked_path: Optional[str]
    script_retry_count: Optional[int]
    canon_violations: List[str]
    is_canon_safe: bool
    canon_pass: bool
    canon_result: Optional[dict]
    
    # Human Approval Gates
    script_approved: bool
    shristi_approved: bool
    priya_shelly_approved: Optional[bool]
    final_cut_approved: bool
    
    # Production Assets (Parallel Branches)
    scene_avatars: Optional[dict]
    avatar_ready: bool
    video_clips_ready: bool
    generated_clips: List[str]
    voiceover_ready: bool
    audio_package_folder: Optional[str]
    music_ready: bool
    sfx_ready: bool
    video_editor_ready: bool
    formatter_ready: bool
    visual_assets: Annotated[List[str], operator.add]
    audio_assets: Annotated[List[str], operator.add]
    vfx_status: str
    audio_status: str
    
    # Final Output
    master_video_path: Optional[str]
    video_s3_path: Optional[str]
    audio_s3_path: Optional[str]
    status: str # 'draft' | 'production' | 'completed' | 'failed'
    published: bool # Added for test compatibility
    
    # Feedback loop
    metrics: Dict[str, float]
    errors: List[str] # Added for test compatibility

def create_initial_state(episode_id: str, season: int, ep_num: int, title_en: str = "", title_hi: str = "") -> EpisodeProductionState:
    return {
        "episode_id": episode_id,
        "season_id": season,
        "title_en": title_en,
        "title_hi": title_hi,
        "script_raw": None,
        "script_final": None,
        "canon_violations": [],
        "is_canon_safe": True,
        "canon_pass": False,
        "script_approved": False,
        "shristi_approved": False,
        "final_cut_approved": False,
        "visual_assets": [],
        "audio_assets": [],
        "vfx_status": "pending",
        "audio_status": "pending",
        "video_s3_path": None,
        "audio_s3_path": None,
        "status": "draft",
        "published": False,
        "metrics": {},
        "errors": []
    }

# Alias for backward compatibility if needed
get_initial_state = create_initial_state
