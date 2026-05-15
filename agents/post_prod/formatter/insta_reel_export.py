"""
Crown of Kaliyug — Instagram Reel Export
A-11 · agents/post_prod/formatter/insta_reel_export.py
9:16 vertical, 60 seconds, most dramatic scene
"""
import os, subprocess
from pathlib import Path
from loguru import logger


def export(master_path: str, episode_id: str, spec: dict) -> str:
    out_path = str(Path("output/final") / f"{episode_id}_instagram_reel.mp4")

    if not os.path.exists(master_path) or not master_path.endswith(".mp4"):
        return _placeholder(episode_id, out_path)

    # 9:16 crop from center + 60 sec from most dramatic moment (SC03 Karna entrance ~5 min mark)
    start_sec = spec.get("teaser_start_sec", 300)
    cmd = [
        "ffmpeg", "-i", master_path,
        "-ss", str(start_sec), "-t", "60",
        "-vf", "crop=ih*9/16:ih,scale=1080:1920",
        "-c:v", "libx264", "-b:v", "3500k",
        "-c:a", "aac",     "-b:a", "128k",
        "-r", "30", out_path, "-y"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.success(f"[A-11] Instagram Reel: {out_path}")
    except Exception as e:
        logger.error(f"[A-11] Reel export failed: {e}")
        return _placeholder(episode_id, out_path)
    return out_path


def _placeholder(episode_id, out_path):
    txt = out_path.replace(".mp4", "_plan.txt")
    with open(txt, "w") as f:
        f.write(f"PLATFORM: instagram_reel\nRESOLUTION: 1080x1920\nDURATION: 60 sec\nSTATUS: Waiting for master video\n")
    return txt
