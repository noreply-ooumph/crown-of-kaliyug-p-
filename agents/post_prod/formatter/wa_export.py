"""
Crown of Kaliyug — WhatsApp Status Export
A-11 · agents/post_prod/formatter/wa_export.py
9:16 vertical, 30 sec, under 16MB
"""
import os, subprocess
from pathlib import Path
from loguru import logger

MAX_SIZE_MB = 16


def export(master_path: str, episode_id: str, spec: dict) -> str:
    out_path = str(Path("output/final") / f"{episode_id}_whatsapp.mp4")

    if not os.path.exists(master_path) or not master_path.endswith(".mp4"):
        return _placeholder(episode_id, out_path)

    start_sec = spec.get("wa_start_sec", 300)
    cmd = [
        "ffmpeg", "-i", master_path,
        "-ss", str(start_sec), "-t", "30",
        "-vf", "crop=ih*9/16:ih,scale=720:1280",
        "-c:v", "libx264", "-b:v", "1500k",
        "-c:a", "aac",     "-b:a", "96k",
        "-r", "24", out_path, "-y"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size_mb = os.path.getsize(out_path) / (1024*1024)
        if size_mb > MAX_SIZE_MB:
            logger.warning(f"[A-11] WA file {size_mb:.1f}MB > 16MB — recompressing")
            _recompress(out_path)
        logger.success(f"[A-11] WhatsApp export: {out_path}")
    except Exception as e:
        logger.error(f"[A-11] WA export failed: {e}")
        return _placeholder(episode_id, out_path)
    return out_path


def _recompress(path):
    tmp = path.replace(".mp4", "_tmp.mp4")
    os.rename(path, tmp)
    subprocess.run([
        "ffmpeg", "-i", tmp, "-b:v", "800k", "-b:a", "64k", path, "-y"
    ], capture_output=True)
    os.remove(tmp)


def _placeholder(episode_id, out_path):
    txt = out_path.replace(".mp4", "_plan.txt")
    with open(txt, "w") as f:
        f.write(f"PLATFORM: whatsapp\nRESOLUTION: 720x1280\nDURATION: 30 sec\nMAX SIZE: 16MB\nSTATUS: Waiting for master video\n")
    return txt
