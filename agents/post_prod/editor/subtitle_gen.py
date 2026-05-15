"""
Crown of Kaliyug — Subtitle Generator
Phase 4 · agents/post_prod/editor/subtitle_gen.py

Generates Hindi primary + English secondary .srt from dialogue transcript.
Method 1: Claude API — from dialogue JSON (preferred)
Method 2: Whisper — from voiceover audio files (fallback)
"""
import json
import os
from pathlib import Path
from loguru import logger


def generate_subtitles(
    episode_id:  str,
    script_path: str,
    voiceover_dir: str = None,
) -> dict:
    """
    Generates .srt files for episode.
    Returns: {hindi_srt, english_srt}
    """
    out_dir = Path("output/final") / episode_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Method 1: From script JSON dialogue (fast, no audio needed)
    try:
        with open(script_path, encoding="utf-8") as f:
            script = json.load(f)
        result = _generate_from_script(script, episode_id, out_dir)
        if result:
            return result
    except Exception as e:
        logger.warning(f"[SubGen] Script method failed: {e}")

    # Method 2: Whisper from voiceover audio (fallback)
    if voiceover_dir and os.path.exists(voiceover_dir):
        return _generate_from_audio(episode_id, voiceover_dir, out_dir)

    return _placeholder_srt(episode_id, out_dir)


def _generate_from_script(script: dict, episode_id: str, out_dir: Path) -> dict | None:
    """Generates bilingual SRT from dialogue slots in script JSON."""
    try:
        from shared.llm.llm_client import call_llm_json
        prompt_path = "prompts/subtitle_generator.txt"
        with open(prompt_path) as f:
            system = f.read()
    except Exception:
        return _build_srt_from_dialogue(script, episode_id, out_dir)

    # Extract all dialogue with character + text
    dialogue_lines = []
    time_cursor    = 0.0
    for scene in script.get("scenes", []):
        if scene.get("is_tag_sequence"):
            time_cursor += 480
            continue
        for slot in scene.get("dialogue_slots", []):
            text = slot.get("text", "")
            if not text:
                continue
            dialogue_lines.append({
                "character": slot.get("character", ""),
                "text":      text,
                "emotion":   slot.get("emotion_tag", "[formal]"),
                "start_sec": round(time_cursor, 2),
            })
            # Estimate 3 sec per line average
            time_cursor += max(2, len(text.split()) * 0.4)

    if not dialogue_lines:
        return None

    # Claude generates English translations
    result = call_llm_json(
        system_prompt=system,
        user_message=json.dumps(dialogue_lines[:50], ensure_ascii=False),
        max_tokens=3000,
    )
    if isinstance(result, list):
        translated = result
    elif isinstance(result, dict):
        translated = result.get("lines", dialogue_lines)
    else:
        translated = dialogue_lines
        
    return _write_srt_files(translated, episode_id, out_dir)


def _build_srt_from_dialogue(script: dict, episode_id: str, out_dir: Path) -> dict:
    """Builds Hindi-only SRT directly from dialogue slots."""
    lines     = []
    time_cur  = 0.0
    for scene in script.get("scenes", []):
        if scene.get("is_tag_sequence"):
            time_cur += 480
            continue
        for slot in scene.get("dialogue_slots", []):
            text = slot.get("text", "")
            if not text:
                continue
            dur = max(2.0, len(text.split()) * 0.4)
            lines.append({
                "character":    slot.get("character", ""),
                "hindi":        text,
                "english":      "",
                "start_sec":    round(time_cur, 2),
                "end_sec":      round(time_cur + dur, 2),
            })
            time_cur += dur
    return _write_srt_files(lines, episode_id, out_dir)


def _write_srt_files(lines: list, episode_id: str, out_dir: Path) -> dict:
    hindi_srt   = str(out_dir / f"{episode_id}_hindi.srt")
    english_srt = str(out_dir / f"{episode_id}_english.srt")
    hi_lines, en_lines = [], []

    for i, line in enumerate(lines, 1):
        start = _fmt(line.get("start_sec", 0))
        end   = _fmt(line.get("end_sec",   line.get("start_sec", 0) + 3))
        char  = line.get("character", "").upper()
        hindi = line.get("hindi", line.get("text", ""))
        eng   = line.get("english", "")

        hi_lines += [str(i), f"{start} --> {end}", f"{char}: {hindi}", ""]
        if eng:
            en_lines += [str(i), f"{start} --> {end}", f"{char}: {eng}", ""]

    with open(hindi_srt,   "w", encoding="utf-8") as f: f.write("\n".join(hi_lines))
    with open(english_srt, "w", encoding="utf-8") as f: f.write("\n".join(en_lines))

    logger.success(f"[SubGen] {len(lines)} lines — Hindi + English SRT generated")
    return {"hindi_srt": hindi_srt, "english_srt": english_srt}


def _generate_from_audio(episode_id, voiceover_dir, out_dir):
    """Whisper fallback — transcribes voiceover MP3 files."""
    try:
        import whisper
        model    = whisper.load_model("base")
        mp3s     = sorted(Path(voiceover_dir).glob("*.mp3"))
        segments = []
        t        = 0.0
        for mp3 in mp3s:
            res = model.transcribe(str(mp3), language="hi")
            for seg in res.get("segments", []):
                segments.append({
                    "hindi":     seg["text"].strip(),
                    "english":   "",
                    "start_sec": t + seg["start"],
                    "end_sec":   t + seg["end"],
                })
            t += res.get("duration", 0)
        return _write_srt_files(segments, episode_id, out_dir)
    except Exception as e:
        logger.error(f"[SubGen] Whisper failed: {e}")
        return _placeholder_srt(episode_id, out_dir)


def _placeholder_srt(episode_id, out_dir):
    path = str(out_dir / f"{episode_id}_placeholder.srt")
    with open(path, "w") as f:
        f.write("1\n00:00:00,000 --> 00:00:05,000\n[Subtitles pending]\n")
    return {"hindi_srt": path, "english_srt": ""}


def _fmt(sec):
    h  = int(sec // 3600)
    m  = int((sec % 3600) // 60)
    s  = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
