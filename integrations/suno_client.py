"""
Crown of Kaliyug - Suno Client
integrations/suno_client.py

Current: stub - logs prompt that would be sent
Production: set SUNO_API_KEY in .env
"""
import os
from loguru import logger

API_KEY = os.getenv("SUNO_API_KEY", "")


def generate_music(prompt: str, duration_sec: int = 30) -> str | None:
    """
    Generate music from prompt.
    Returns S3/local path to generated .mp3 or None if not configured.
    """
    if not API_KEY:
        logger.warning(f"[Suno] API key not set. Would generate: {prompt[:80]}")
        return None
    # TODO: implement when Suno API is available
    logger.info(f"[Suno] Generating: {prompt[:80]}")
    return None


def generate_from_theme(theme: dict) -> str | None:
    prompt = theme.get("suno_prompt", "")
    return generate_music(prompt)
