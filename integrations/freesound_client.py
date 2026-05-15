"""
Crown of Kaliyug - Freesound Client
integrations/freesound_client.py

Current: stub - logs what would be fetched
Production: set FREESOUND_API_KEY in .env
Register free at: https://freesound.org/apiv2/apply/
"""
import os
import requests
from loguru import logger

API_KEY  = os.getenv("FREESOUND_API_KEY", "")
BASE_URL = "https://freesound.org/apiv2"


def search(query: str, max_results: int = 5) -> list:
    if not API_KEY:
        logger.warning(f"[Freesound] API key not set. Would search: {query}")
        return []
    resp = requests.get(
        f"{BASE_URL}/search/text/",
        params={"query": query, "page_size": max_results, "fields": "id,name,previews"},
        headers={"Authorization": f"Token {API_KEY}"},
    )
    return resp.json().get("results", []) if resp.status_code == 200 else []


def download(sound_id: int, out_path: str) -> bool:
    if not API_KEY:
        logger.warning(f"[Freesound] API key not set. Would download: {sound_id}")
        return False
    resp = requests.get(
        f"{BASE_URL}/sounds/{sound_id}/",
        headers={"Authorization": f"Token {API_KEY}"},
    )
    if resp.status_code != 200:
        return False
    preview = resp.json().get("previews", {}).get("preview-hq-mp3", "")
    if not preview:
        return False
    audio = requests.get(preview)
    with open(out_path, "wb") as f:
        f.write(audio.content)
    return True
