"""
Crown of Kaliyug — Video Generation Agent (A-06)
Phase 2 · agents/visual_prod/video/video_agent.py

Mode: D-ID API (lip sync + talking head)
Fallback: Ken Burns (if D-ID fails)
"""
import os
import json
import time
import requests
import base64
from pathlib import Path
from loguru import logger
from agents.visual_prod.avatar.avatar_agent import get_avatar, get_scene_primary_avatar

VIDEO_DIR   = Path("output/video")
AUDIO_DIR   = Path("output/audio")
DID_API_KEY = os.getenv("DID_API_KEY", "")
VIDEO_MODE  = os.getenv("VIDEO_MODE", "did")

DID_BASE    = "https://api.d-id.com"

KB_PRESETS = {
    "power":      {"zoom_start": 1.0,  "zoom_end": 1.15, "direction": "center"},
    "dramatic":   {"zoom_start": 1.15, "zoom_end": 1.0,  "direction": "left"},
    "intimate":   {"zoom_start": 1.0,  "zoom_end": 1.2,  "direction": "right"},
    "suspense":   {"zoom_start": 1.2,  "zoom_end": 1.05, "direction": "center"},
    "revelation": {"zoom_start": 1.3,  "zoom_end": 1.0,  "direction": "center"},
    "default":    {"zoom_start": 1.0,  "zoom_end": 1.1,  "direction": "center"},
}

SCENE_MOODS = {
    "S1E01-SC01": "power",
    "S1E01-SC02": "dramatic",
    "S1E01-SC03": "revelation",
    "S1E01-SC04": "intimate",
    "S1E01-SC05": "suspense",
}

WPS = 2.5  # words per second


def run(state: dict) -> dict:
    episode_id  = state["episode_id"]
    script_path = state.get("script_draft_path") or state.get("script_locked_path", "")

    logger.info(f"[A-06] Video Agent — {episode_id} | Mode: D-ID lip sync")

    try:
        with open(script_path, encoding="utf-8") as f:
            script = json.load(f)
    except Exception as e:
        logger.error(f"[A-06] Script load failed: {e}")
        state["errors"] = state.get("errors", []) + [str(e)]
        return state

    out_dir = VIDEO_DIR / episode_id
    out_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for scene in script.get("scenes", []):
        scene_id = scene.get("scene_id", "")
        is_tag   = scene.get("is_tag_sequence", False)
        mood     = SCENE_MOODS.get(scene_id, "default")
        out_path = str(out_dir / f"{scene_id}.mp4")

        if is_tag:
            success = _black_screen(out_path, 480)
        else:
            slots = scene.get("dialogue_slots", [])
            if slots and DID_API_KEY:
                success = _generate_did_cuts(scene_id, slots, mood, episode_id, out_path, scene)
            elif slots:
                success = _generate_kb_cuts(scene_id, slots, mood, episode_id, out_path, scene)
            else:
                chars    = scene.get("characters_present", [])
                avatar   = get_scene_primary_avatar(chars)
                duration = 30
                success  = _ken_burns(avatar, out_path, duration,
                                      KB_PRESETS.get(mood, KB_PRESETS["default"]), scene_id)

        if success:
            generated.append(scene_id)
            logger.info(f"[A-06] Generated: {scene_id}")

    state["video_clips_ready"] = len(generated) > 0
    state["generated_clips"]   = generated
    logger.success(f"[A-06] {len(generated)}/{len(script.get('scenes', []))} clips for {episode_id}")
    return state


def _generate_did_cuts(scene_id, slots, mood, episode_id, out_path, scene):
    """Generates D-ID talking head clips per dialogue line, then stitches."""
    from moviepy.editor import VideoFileClip, concatenate_videoclips

    tmp_dir = Path("output/video") / episode_id / f"{scene_id}_parts"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    clip_parts  = []
    preset      = KB_PRESETS.get(mood, KB_PRESETS["default"])
    audio_dir   = Path("output/audio") / episode_id / "voiceover"

    # Establishing shot (5 sec Ken Burns)
    chars   = scene.get("characters_present", [])
    primary = get_scene_primary_avatar(chars or [s.get("character","") for s in slots])
    estab   = str(tmp_dir / "00_establishing.mp4")
    if _ken_burns(primary, estab, 5.0, preset, "establishing"):
        try:
            clip_parts.append(VideoFileClip(estab))
        except:
            pass

    for i, slot in enumerate(slots):
        character = slot.get("character", "")
        text      = slot.get("text", "")
        slot_id   = slot.get("slot_id", f"{scene_id}-L{i+1:02d}")

        avatar_path = get_avatar(character)
        if not avatar_path:
            avatar_path = get_scene_primary_avatar([character])

        # Find voiceover audio
        audio_path = _find_audio(audio_dir, slot_id, scene_id, i)
        tmp_path   = str(tmp_dir / f"line_{i+1:02d}_{character}.mp4")

        if audio_path and avatar_path:
            success = _did_talking_head(avatar_path, audio_path, tmp_path, character, slot_id)
        elif avatar_path:
            duration = max(4.0, len(text.split()) / WPS)
            success  = _ken_burns(avatar_path, tmp_path, duration, preset, character)
        else:
            success = False

        if success and os.path.exists(tmp_path):
            try:
                clip_parts.append(VideoFileClip(tmp_path))
                logger.debug(f"[A-06] Added: {character} — {text[:40]}...")
            except Exception as e:
                logger.warning(f"[A-06] Clip load failed: {e}")

    if not clip_parts:
        return _fallback_color(out_path, 60, scene_id)

    try:
        final = concatenate_videoclips(clip_parts, method="compose")
        final.write_videofile(out_path, fps=24, codec="libx264",
                              bitrate="4000k", audio=True, logger=None)
        logger.success(f"[A-06] D-ID scene: {scene_id} ({len(clip_parts)} cuts, {final.duration:.1f}s)")
        return True
    except Exception as e:
        logger.error(f"[A-06] Stitch failed: {e}")
        return False


def _did_talking_head(avatar_path, audio_path, out_path, character, slot_id):
    """
    Calls D-ID API to generate talking head video.
    Input:  portrait PNG + audio MP3
    Output: lip sync MP4
    """
    try:
        headers = {
            "Authorization": f"Basic {DID_API_KEY}",
            "Content-Type":  "application/json",
            "Accept":        "application/json",
        }

        # Upload image to D-ID
        with open(avatar_path, "rb") as f:
            img_data = f.read()
        img_b64  = base64.b64encode(img_data).decode()
        img_url  = f"data:image/png;base64,{img_b64}"

        # Upload audio to D-ID
        with open(audio_path, "rb") as f:
            aud_data = f.read()
        aud_b64 = base64.b64encode(aud_data).decode()
        aud_url = f"data:audio/mp3;base64,{aud_b64}"

        # Create talk
        payload = {
            "source_url": img_url,
            "script": {
                "type":       "audio",
                "audio_url":  aud_url,
            },
            "config": {
                "stitch":    True,
                "result_format": "mp4",
            }
        }

        logger.info(f"[A-06] D-ID: Creating talk for {character}...")
        resp = requests.post(f"{DID_BASE}/talks", json=payload, headers=headers, timeout=60)

        if resp.status_code not in (200, 201):
            logger.warning(f"[A-06] D-ID create failed {resp.status_code}: {resp.text[:200]}")
            return False

        talk_id = resp.json().get("id")
        if not talk_id:
            logger.warning(f"[A-06] No talk ID returned")
            return False

        logger.info(f"[A-06] D-ID talk created: {talk_id} — polling...")

        # Poll for completion
        for attempt in range(30):
            time.sleep(3)
            poll = requests.get(f"{DID_BASE}/talks/{talk_id}", headers=headers, timeout=30)
            if poll.status_code != 200:
                continue
            data   = poll.json()
            status = data.get("status", "")

            if status == "done":
                video_url = data.get("result_url", "")
                if not video_url:
                    logger.warning(f"[A-06] No result URL")
                    return False
                # Download video
                video_resp = requests.get(video_url, timeout=60)
                with open(out_path, "wb") as f:
                    f.write(video_resp.content)
                logger.success(f"[A-06] D-ID done: {character} → {out_path}")
                return True
            elif status == "error":
                logger.error(f"[A-06] D-ID error: {data.get('error', '')}")
                return False
            else:
                logger.debug(f"[A-06] D-ID status: {status} (attempt {attempt+1})")

        logger.warning(f"[A-06] D-ID timeout for {slot_id}")
        return False

    except Exception as e:
        logger.error(f"[A-06] D-ID failed: {e}")
        return False


def _generate_kb_cuts(scene_id, slots, mood, episode_id, out_path, scene):
    """Ken Burns cuts fallback — no D-ID API."""
    from moviepy.editor import VideoFileClip, concatenate_videoclips

    tmp_dir = Path("output/video") / episode_id / f"{scene_id}_parts"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    preset  = KB_PRESETS.get(mood, KB_PRESETS["default"])
    parts   = []

    for i, slot in enumerate(slots):
        character = slot.get("character", "")
        text      = slot.get("text", "")
        avatar    = get_avatar(character) or get_scene_primary_avatar([character])
        duration  = max(4.0, len(text.split()) / WPS)
        tmp_path  = str(tmp_dir / f"line_{i+1:02d}_{character}.mp4")

        if _ken_burns(avatar, tmp_path, duration, preset, character):
            try:
                parts.append(VideoFileClip(tmp_path))
            except:
                pass

    if not parts:
        return _fallback_color(out_path, 60, scene_id)

    try:
        concatenate_videoclips(parts, method="compose").write_videofile(
            out_path, fps=24, codec="libx264", bitrate="4000k", audio=False, logger=None)
        return True
    except Exception as e:
        logger.error(f"[A-06] KB cuts failed: {e}")
        return False


def _find_audio(audio_dir, slot_id, scene_id, idx):
    if not audio_dir.exists():
        return ""
    candidates = (list(audio_dir.glob(f"*{slot_id}*")) or
                  list(audio_dir.glob(f"*{scene_id}*L{idx+1:02d}*")) or
                  list(audio_dir.glob(f"*{scene_id}*.mp3")))
    return str(candidates[idx]) if idx < len(candidates) else (str(candidates[0]) if candidates else "")


def _ken_burns(avatar_path, out_path, duration, preset, label):
    try:
        import numpy as np
        from moviepy.editor import VideoClip
        from PIL import Image

        if not avatar_path or not os.path.exists(avatar_path):
            return _fallback_color(out_path, duration, label)

        img     = Image.open(avatar_path).convert("RGB")
        img_arr = np.array(img)
        h, w    = img_arr.shape[:2]
        z_s     = preset["zoom_start"]
        z_e     = preset["zoom_end"]

        def make_frame(t):
            progress = t / max(duration, 0.1)
            zoom  = z_s + (z_e - z_s) * progress
            new_w = max(1, int(w / zoom))
            new_h = max(1, int(h / zoom))
            x = (w - new_w) // 2
            y = (h - new_h) // 2
            x = max(0, min(x, w - new_w))
            y = max(0, min(y, h - new_h))
            crop = img_arr[y:y+new_h, x:x+new_w]
            return np.array(Image.fromarray(crop).resize((1920, 1080), Image.LANCZOS))

        VideoClip(make_frame, duration=duration).write_videofile(
            out_path, fps=24, codec="libx264", bitrate="3000k", audio=False, logger=None)
        return True
    except Exception as e:
        logger.error(f"[A-06] Ken Burns failed: {e}")
        return _fallback_color(out_path, duration, label)


def _black_screen(out_path, duration):
    try:
        from moviepy.editor import ColorClip
        ColorClip(size=(1920,1080), color=(0,0,0), duration=duration).write_videofile(
            out_path, fps=24, codec="libx264", audio=False, logger=None)
        return True
    except Exception as e:
        logger.error(f"[A-06] Black screen failed: {e}")
        return False


def _fallback_color(out_path, duration, label):
    try:
        from moviepy.editor import ColorClip
        ColorClip(size=(1920,1080), color=(20,20,30), duration=max(1,duration)).write_videofile(
            out_path, fps=24, codec="libx264", audio=False, logger=None)
        return True
    except Exception as e:
        logger.error(f"[A-06] Fallback failed: {e}")
        return False
