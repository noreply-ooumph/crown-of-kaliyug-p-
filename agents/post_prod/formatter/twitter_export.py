"""
Crown of Kaliyug — Twitter/X Export
A-11 · agents/post_prod/formatter/twitter_export.py
1:1 square, 30 seconds hook
"""
import os, subprocess
from pathlib import Path
from loguru import logger


def export(master_path: str, episode_id: str, spec: dict) -> str:
    out_path = str(Path("output/final") / f"{episode_id}_twitter.mp4")

    if not os.path.exists(master_path) or not master_path.endswith(".mp4"):
        return _placeholder(episode_id, out_path)

    start_sec = spec.get("hook_start_sec", 120)
    cmd = [
        "ffmpeg", "-i", master_path,
        "-ss", str(start_sec), "-t", "30",
        "-vf", r"crop=min(iw\,ih):min(iw\,ih),scale=1080:1080",
        "-c:v", "libx264", "-b:v", "2500k",
        "-c:a", "aac",     "-b:a", "128k",
        "-r", "24", out_path, "-y"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.success(f"[A-11] Twitter export: {out_path}")
    except Exception as e:
        logger.error(f"[A-11] Twitter export failed: {e}")
        return _placeholder(episode_id, out_path)
    return out_path


def _placeholder(episode_id, out_path):
    txt = out_path.replace(".mp4", "_plan.txt")
    with open(txt, "w") as f:
        f.write(f"PLATFORM: twitter\nRESOLUTION: 1080x1080\nDURATION: 30 sec\nSTATUS: Waiting for master video\n")
    return txt
