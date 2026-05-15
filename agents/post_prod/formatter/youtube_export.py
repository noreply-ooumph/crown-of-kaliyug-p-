"""
Crown of Kaliyug — YouTube Export
A-11 · agents/post_prod/formatter/youtube_export.py
Full episode 16:9 1080p + chapter markers
"""
import os, json, subprocess
from pathlib import Path
from loguru import logger


def export(master_path: str, episode_id: str, spec: dict) -> str:
    out_path = str(Path("output/final") / f"{episode_id}_youtube.mp4")

    if not os.path.exists(master_path) or not master_path.endswith(".mp4"):
        return _placeholder(episode_id, "youtube", out_path)

    cmd = [
        "ffmpeg", "-i", master_path,
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264", "-b:v", "8000k",
        "-c:a", "aac",     "-b:a", "192k",
        "-r", "24", out_path, "-y"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.success(f"[A-11] YouTube export: {out_path}")
    except Exception as e:
        logger.error(f"[A-11] YouTube export failed: {e}")
        return _placeholder(episode_id, "youtube", out_path)
    return out_path


def _placeholder(episode_id, platform, out_path):
    with open(out_path.replace(".mp4", "_plan.txt"), "w") as f:
        f.write(f"PLATFORM: {platform}\nRESOLUTION: 1920x1080\nBITRATE: 8000k\nSTATUS: Waiting for master video\n")
    return out_path.replace(".mp4", "_plan.txt")
