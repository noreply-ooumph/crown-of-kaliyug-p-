"""
Crown of Kaliyug — Audio Mixer
Phase 4 · agents/post_prod/editor/audio_mixer.py

Mixing rules (Series Bible):
  Voiceover:  0dB   (primary, never ducked)
  BG Music:  -18dB  during dialogue scenes
  BG Music:   -8dB  during instrumental/tag scenes
  SFX:       -6dB   timed to action_line timestamps
"""
import os
from pathlib import Path
from loguru import logger


VOICEOVER_DB  =  0    # primary — never duck
MUSIC_DIAL_DB = -18   # during dialogue
MUSIC_INST_DB =  -8   # instrumental / tag scenes
SFX_DB        =  -6   # sound effects


def mix_scene_audio(
    episode_id: str,
    scene_id:   str,
    is_tag:     bool,
    has_dialogue: bool,
) -> str | None:
    """
    Mixes voiceover + music + SFX for a scene.
    Returns path to mixed .mp3 or None if audio not ready.
    """
    audio_base = Path("output/audio") / episode_id
    vo_dir     = audio_base / "voiceover"
    music_dir  = audio_base / "music"
    sfx_dir    = audio_base / "sfx"
    out_dir    = audio_base / "mixed"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from pydub import AudioSegment
        from pydub.effects import normalize
    except ImportError:
        logger.warning("[Mixer] pydub not installed. Run: pip install pydub")
        return None

    mixed = None

    # ── Voiceover (0dB, only if not tag) ────────────────────────
    if not is_tag and has_dialogue:
        vo_files = sorted(vo_dir.glob(f"{scene_id}*.mp3")) if vo_dir.exists() else []
        if vo_files:
            vo_combined = sum(
                (AudioSegment.from_mp3(str(f)) for f in vo_files),
                AudioSegment.empty()
            )
            mixed = vo_combined + VOICEOVER_DB

    # ── Background music ─────────────────────────────────────────
    music_path = music_dir / f"{scene_id}_music.mp3"
    if music_path.exists():
        music     = AudioSegment.from_mp3(str(music_path))
        music_vol = MUSIC_DIAL_DB if (has_dialogue and not is_tag) else MUSIC_INST_DB
        music_adj = music + music_vol

        if mixed:
            # Overlay music under voiceover
            if len(music_adj) < len(mixed):
                music_adj = music_adj * (len(mixed) // len(music_adj) + 1)
            mixed = mixed.overlay(music_adj[:len(mixed)])
        else:
            mixed = music_adj

    # ── SFX layer ────────────────────────────────────────────────
    sfx_files = list(sfx_dir.glob(f"{scene_id}*.mp3")) if sfx_dir.exists() else []
    for sfx_file in sfx_files:
        try:
            sfx = AudioSegment.from_mp3(str(sfx_file)) + SFX_DB
            if mixed:
                mixed = mixed.overlay(sfx)
        except Exception as e:
            logger.warning(f"[Mixer] SFX overlay failed: {sfx_file.name}: {e}")

    if mixed is None:
        logger.warning(f"[Mixer] No audio for {scene_id}")
        return None

    out_path = str(out_dir / f"{scene_id}_mixed.mp3")
    mixed.export(out_path, format="mp3")
    logger.debug(f"[Mixer] Mixed: {scene_id} -> {out_path}")
    return out_path
