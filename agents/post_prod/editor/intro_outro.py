"""
Crown of Kaliyug — Intro / Outro Branding
Phase 4 · agents/post_prod/editor/intro_outro.py

Adds:
  - Crown of Kaliyug intro bumper (5 sec)
  - End card with OTT platform CTA
  - Ooumph Networks credit
"""
import os
from pathlib import Path
from loguru import logger

BUMPER_PATH   = "assets/branding/cok_intro_bumper.mp4"
END_CARD_PATH = "assets/branding/cok_end_card.mp4"


def get_intro_clip():
    """Returns intro bumper clip or None if not available yet."""
    if os.path.exists(BUMPER_PATH) and os.path.getsize(BUMPER_PATH) > 0:
        try:
            from moviepy import VideoFileClip
            clip = VideoFileClip(BUMPER_PATH)
            logger.info(f"[Branding] Intro bumper loaded: {clip.duration:.1f}s")
            return clip
        except Exception as e:
            logger.error(f"[Branding] Failed to load intro: {e}")
    else:
        logger.warning(f"[Branding] Intro bumper missing or 0 bytes: {BUMPER_PATH}")
    return None


def get_outro_clip():
    """Returns end card clip or None if not available yet."""
    if os.path.exists(END_CARD_PATH) and os.path.getsize(END_CARD_PATH) > 0:
        try:
            from moviepy import VideoFileClip
            clip = VideoFileClip(END_CARD_PATH)
            logger.info(f"[Branding] End card loaded: {clip.duration:.1f}s")
            return clip
        except Exception as e:
            logger.error(f"[Branding] Failed to load end card: {e}")
    else:
        logger.warning(f"[Branding] End card missing or 0 bytes: {END_CARD_PATH}")
    return None


def branding_status() -> dict:
    return {
        "intro_bumper": "ready" if (os.path.exists(BUMPER_PATH) and os.path.getsize(BUMPER_PATH) > 0) else "MISSING",
        "end_card":     "ready" if (os.path.exists(END_CARD_PATH) and os.path.getsize(END_CARD_PATH) > 0) else "MISSING",
    }
