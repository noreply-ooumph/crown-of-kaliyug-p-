"""
Crown of Kaliyug — Platform Formatter Agent (A-11)
Phase 4 · agents/post_prod/formatter/formatter_agent.py

Takes master episode file → 5 platform cuts:
  YouTube        16:9  full episode
  Instagram Reel  9:16  60 sec teaser
  Twitter         1:1   30 sec hook
  WhatsApp        9:16  30 sec under 16MB
  Thumbnail      16:9  1280x720 PNG

HITL Gate: Priya/Shelly approve master.mp4 before this runs.
"""
import json
from pathlib import Path
from loguru import logger

from agents.post_prod.formatter.youtube_export    import export as yt_export
from agents.post_prod.formatter.insta_reel_export import export as reel_export
from agents.post_prod.formatter.twitter_export    import export as tw_export
from agents.post_prod.formatter.wa_export         import export as wa_export
from agents.post_prod.formatter.thumbnail_gen     import generate as thumb_gen

OUTPUT_DIR = Path("output/final")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run(state: dict) -> dict:
    episode_id  = state["episode_id"]
    master_path = state.get("master_video_path", "")

    logger.info(f"[A-11] Platform Formatter — {episode_id}")

    # HITL check — Priya/Shelly must approve before exporting
    if not state.get("priya_shelly_approved", False):
        logger.warning(f"[A-11] Waiting for Priya/Shelly approval on master.mp4")
        state["formatter_ready"] = False
        state["formatter_status"] = "PENDING_APPROVAL"
        _save_approval_request(episode_id, master_path)
        return state

    # Load platform specs
    try:
        import yaml
        with open("config/platform_specs.yaml") as f:
            specs = yaml.safe_load(f) or {}
    except Exception:
        specs = {}

    outputs = {}

    # Run all platform exports
    exporters = [
        ("youtube",        lambda: yt_export(master_path,   episode_id, specs.get("youtube", {}))),
        ("instagram_reel", lambda: reel_export(master_path, episode_id, specs.get("instagram_reel", {}))),
        ("twitter",        lambda: tw_export(master_path,   episode_id, specs.get("twitter", {}))),
        ("whatsapp",       lambda: wa_export(master_path,   episode_id, specs.get("whatsapp", {}))),
        ("thumbnail",      lambda: thumb_gen(master_path,   episode_id, specs.get("thumbnail", {}))),
    ]

    for platform, fn in exporters:
        try:
            out_path = fn()
            outputs[platform] = {"path": out_path, "status": "ready"}
            logger.info(f"[A-11] {platform:15} -> {out_path}")
        except Exception as e:
            logger.error(f"[A-11] {platform} failed: {e}")
            outputs[platform] = {"path": "", "status": f"failed: {e}"}

    state["platform_outputs"] = outputs
    state["formatter_ready"]  = True

    # Save outputs summary
    summary_path = str(OUTPUT_DIR / f"{episode_id}_platform_outputs.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2)

    logger.success(f"[A-11] All platforms done — {len(outputs)} exports")
    return state


def _save_approval_request(episode_id: str, master_path: str):
    """Saves approval request — Priya/Shelly review master.mp4 via WA."""
    req = {
        "episode_id":   episode_id,
        "master_path":  master_path,
        "status":       "PENDING_APPROVAL",
        "instructions": "Review master.mp4 and set priya_shelly_approved=True in state to proceed",
        "approve_action": "Set state['priya_shelly_approved'] = True",
        "reject_action":  "Set state['edit_notes'] = 'timestamp + note' and re-run A-10",
    }
    req_path = str(OUTPUT_DIR / f"{episode_id}_approval_request.json")
    with open(req_path, "w") as f:
        import json
        json.dump(req, f, indent=2)
    logger.info(f"[A-11] Approval request saved -> {req_path}")
    logger.info(f"[A-11] Send master.mp4 to Priya/Shelly via WhatsApp for review")
