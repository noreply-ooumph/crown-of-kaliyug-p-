"""
Crown of Kaliyug — Thumbnail Generator
A-11 · agents/post_prod/formatter/thumbnail_gen.py
1280x720 PNG from most dramatic frame (Karna entrance / coronation)
"""
import os, subprocess
from pathlib import Path
from loguru import logger


def generate(master_path: str, episode_id: str, spec: dict) -> str:
    out_path = str(Path("output/final") / f"{episode_id}_thumbnail.png")

    if not os.path.exists(master_path) or not master_path.endswith(".mp4"):
        return _placeholder(episode_id, out_path)

    # Extract frame from SC03 Karna entrance — most dramatic visual moment
    frame_sec = spec.get("thumbnail_frame_sec", 320)
    cmd = [
        "ffmpeg", "-i", master_path,
        "-ss", str(frame_sec), "-vframes", "1",
        "-vf", "scale=1280:720",
        "-q:v", "2", out_path, "-y"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.success(f"[A-11] Thumbnail: {out_path}")
    except Exception as e:
        logger.error(f"[A-11] Thumbnail failed: {e}")
        return _placeholder(episode_id, out_path)
    return out_path


def _placeholder(episode_id, out_path):
    txt = out_path.replace(".png", "_plan.txt")
    with open(txt, "w") as f:
        f.write(f"PLATFORM: thumbnail\nRESOLUTION: 1280x720\nFORMAT: PNG\nSTATUS: Waiting for master video\n")
    return txt
