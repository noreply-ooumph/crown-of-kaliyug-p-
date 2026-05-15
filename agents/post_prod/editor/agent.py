"""
Crown of Kaliyug — Video Editor Agent (A-10)
Phase 4 · agents/post_prod/editor/agent.py

Full assembly pipeline:
  Intro bumper → Scenes (video + mixed audio) → Tag sequence → End card
  + Subtitles burned in → master.mp4

Placeholder mode: when A-06 clips not ready → saves assembly plan JSON
Production mode:  when A-06 clips ready → full moviepy assembly
"""
import json
from pathlib import Path
from loguru import logger

from agents.post_prod.editor.scene_sequencer import get_ordered_clips, validate_sequence
from agents.post_prod.editor.audio_mixer     import mix_scene_audio
from agents.post_prod.editor.tag_enforcer    import enforce_tag_rules, validate_tag_clip
from agents.post_prod.editor.subtitle_gen    import generate_subtitles
from agents.post_prod.editor.intro_outro     import get_intro_clip, get_outro_clip, branding_status

OUTPUT_DIR = Path("output/final")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run(state: dict) -> dict:
    episode_id  = state["episode_id"]
    season      = state.get("season", 1)
    script_path = state.get("script_locked_path") or state.get("script_draft_path", "")

    logger.info(f"[A-10] Video Editor — {episode_id}")

    # Load script
    try:
        with open(script_path, encoding="utf-8") as f:
            script = json.load(f)
    except Exception as e:
        logger.error(f"[A-10] Script load failed: {e}")
        state["errors"] = state.get("errors", []) + [str(e)]
        return state

    scenes = script.get("scenes", [])
    clips  = get_ordered_clips(episode_id, scenes)

    # Check if video clips ready
    all_ready = validate_sequence(clips)

    if all_ready:
        logger.info("[A-10] All clips ready — full assembly")
        out_path = _full_assembly(episode_id, scenes, clips, script_path, state)
    else:
        logger.warning("[A-10] Clips pending (A-06) — saving assembly plan")
        out_path = _save_assembly_plan(episode_id, scenes, clips, script_path)

    state["master_video_path"]  = out_path
    state["video_editor_ready"] = True
    logger.success(f"[A-10] Done -> {out_path}")
    return state


def _full_assembly(episode_id, scenes, clips, script_path, state):
    """Full moviepy assembly — runs when all A-06 clips are ready."""
    try:
        from moviepy.editor import concatenate_videoclips, VideoFileClip
    except ImportError:
        logger.error("[A-10] moviepy not installed")
        return _save_assembly_plan(episode_id, scenes, clips, script_path)

    final_clips = []

    # ── 1. Intro bumper ────────────────────────────────────────────
    intro = get_intro_clip()
    if intro:
        final_clips.append(intro)

    # ── 2. Scene assembly ──────────────────────────────────────────
    for clip_info in clips:
        scene_id = clip_info["scene_id"]
        is_tag   = clip_info["is_tag"]

        # Get matching scene from script
        scene = next((s for s in scenes if s.get("scene_id") == scene_id), {})
        has_dialogue = bool(scene.get("dialogue_slots"))

        # Build clip config
        clip_cfg = {
            "voiceover_enabled": True,
            "dialogue_enabled":  True,
            "subtitle_enabled":  True,
            "music_enabled":     True,
            "music_volume_db":   -18 if has_dialogue else -8,
        }

        # Enforce tag rules (non-overridable)
        clip_cfg = enforce_tag_rules(scene, clip_cfg)
        if not validate_tag_clip(scene, clip_cfg):
            logger.error(f"[A-10] Tag validation failed for {scene_id}")

        # Load video clip
        try:
            video = VideoFileClip(clip_info["video_path"])
        except Exception as e:
            logger.error(f"[A-10] Could not load {scene_id}: {e}")
            continue

        # Mix audio
        mixed_audio = mix_scene_audio(
            episode_id, scene_id, is_tag, has_dialogue
        )
        if mixed_audio:
            try:
                from moviepy.editor import AudioFileClip
                audio = AudioFileClip(mixed_audio)
                video = video.set_audio(audio)
            except Exception as e:
                logger.warning(f"[A-10] Audio set failed {scene_id}: {e}")

        final_clips.append(video)
        logger.info(f"[A-10] Added: {scene_id} ({'TAG' if is_tag else 'scene'})")

    # ── 3. End card ────────────────────────────────────────────────
    outro = get_outro_clip()
    if outro:
        final_clips.append(outro)

    if not final_clips:
        logger.error("[A-10] No clips to assemble")
        return _save_assembly_plan(episode_id, scenes, clips, script_path)

    # ── 4. Concatenate ─────────────────────────────────────────────
    logger.info(f"[A-10] Concatenating {len(final_clips)} clips...")
    final = concatenate_videoclips(final_clips, method="compose")

    master_path = str(OUTPUT_DIR / f"{episode_id}_master.mp4")
    final.write_videofile(
        master_path, codec="libx264",
        audio_codec="aac", fps=24, logger=None
    )

    # ── 5. Generate subtitles ──────────────────────────────────────
    vo_dir = str(Path("output/audio") / episode_id / "voiceover")
    srt    = generate_subtitles(episode_id, script_path, vo_dir)

    # ── 6. Burn subtitles into master (ffmpeg) ─────────────────────
    if srt.get("hindi_srt"):
        final_with_subs = str(OUTPUT_DIR / f"{episode_id}_master_subtitled.mp4")
        _burn_subtitles(master_path, srt["hindi_srt"], final_with_subs)
        master_path = final_with_subs

    return master_path


def _burn_subtitles(video_path, srt_path, out_path):
    """Burns subtitles into video using ffmpeg."""
    import subprocess
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontName=Noto Sans,FontSize=20,PrimaryColour=&HFFFFFF'",
        "-c:a", "copy", out_path, "-y"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.success(f"[A-10] Subtitles burned: {out_path}")
    except Exception as e:
        logger.warning(f"[A-10] Subtitle burn failed: {e}")


def _save_assembly_plan(episode_id, scenes, clips, script_path):
    """Saves assembly plan JSON when clips not ready."""
    branding = branding_status()
    plan = {
        "episode_id":   episode_id,
        "status":       "PENDING — waiting for A-06 video clips from Anagh",
        "branding":     branding,
        "total_scenes": len(scenes),
        "clips": [
            {
                "scene_id":     c["scene_id"],
                "video_path":   c["video_path"],
                "video_status": "READY" if c["video_exists"] else "PENDING (A-06)",
                "is_tag":       c["is_tag"],
                "location":     c["location"],
            }
            for c in clips
        ],
    }
    out_path = str(OUTPUT_DIR / f"{episode_id}_assembly_plan.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    logger.info(f"[A-10] Assembly plan saved -> {out_path}")
    return out_path
