"""
Crown of Kaliyug - ElevenLabs Client
integrations/elevenlabs_client.py

Current: stub - returns mock response
Production: set ELEVENLABS_API_KEY in .env
"""
import os
import requests
from loguru import logger

API_KEY  = os.getenv("ELEVENLABS_API_KEY", "")
BASE_URL = "https://api.elevenlabs.io/v1"


def generate_speech(text: str, voice_id: str, settings: dict) -> bytes | None:
    if not API_KEY:
        logger.warning("[ElevenLabs] API key not set - returning None")
        return None
    url     = f"{BASE_URL}/text-to-speech/{voice_id}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": settings,
    }
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code == 200:
        return resp.content
    logger.error(f"[ElevenLabs] {resp.status_code}: {resp.text[:200]}")
    return None


def list_voices() -> list:
    if not API_KEY:
        return []
    resp = requests.get(f"{BASE_URL}/voices", headers={"xi-api-key": API_KEY})
    return resp.json().get("voices", []) if resp.status_code == 200 else []
