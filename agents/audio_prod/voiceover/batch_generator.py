"""
Crown of Kaliyug - Batch Voice Generator
A-07 - agents/audio_prod/voiceover/batch_generator.py
Batches dialogue lines for efficient generation.
"""
import asyncio
import os
from pathlib import Path
from loguru import logger
from agents.audio_prod.voiceover.voice_profiles import get_edge_voice
from agents.audio_prod.voiceover.emotion_mapper import get_edge_params


async def generate_line_edge(text: str, character: str,
                              emotion_tag: str, out_path: Path):
    """Generate a single dialogue line using Edge TTS."""
    try:
        import edge_tts
        from agents.audio_prod.voiceover.voice_profiles import get_character_profile
        
        voice  = get_edge_voice(character)
        profile = get_character_profile(character)
        
        # Load character defaults
        char_rate = profile.get("rate", "0%")
        char_pitch = profile.get("pitch", "0Hz")
        
        # Load emotion overrides
        params = get_edge_params(emotion_tag)
        
        # Simple override logic: character defaults are used
        # If emotion is not [formal], we might want to blend, but per instructions
        # we will use the calculated values. 
        # Actually, let's use the character defaults as the base.
        
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=char_rate,
            pitch=char_pitch,
            volume=params["volume"],
        )
        await communicate.save(str(out_path))
        return True
    except Exception as e:
        logger.error(f"Edge TTS failed for {character} [{emotion_tag}]: {e}")
        _save_placeholder(text, character, emotion_tag, out_path)
        return False


def generate_batch_edge(lines: list, out_dir: Path) -> int:
    """
    Batch generate all dialogue lines using Edge TTS.
    lines: list of {text, character, emotion_tag, slot_id}
    Returns count of successfully generated files.
    """
    async def run_all():
        tasks = []
        for line in lines:
            if not line.get("text"):
                continue
            out_path = out_dir / f"{line['slot_id']}.mp3"
            tasks.append(generate_line_edge(
                line["text"],
                line["character"],
                line.get("emotion_tag", "[formal]"),
                out_path
            ))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True)

    return asyncio.run(run_all())


def _save_placeholder(text, character, emotion_tag, out_path):
    txt = str(out_path).replace(".mp3", "_placeholder.txt")
    with open(txt, "w", encoding="utf-8") as f:
        f.write(f"CHARACTER: {character}\nEMOTION: {emotion_tag}\nTEXT: {text}\n")
