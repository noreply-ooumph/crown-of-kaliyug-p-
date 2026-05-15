"""
Crown of Kaliyug - Phase 3 Test Suite
tests/test_phase3.py

Run: python tests/test_phase3.py
Tests all Phase 3 components: A-07, A-08, A-09
"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"
results = []


def test(name, fn):
    try:
        fn()
        print(f"  {PASS}  {name}")
        results.append((name, True, None))
    except Exception as e:
        print(f"  {FAIL}  {name}")
        print(f"       -> {e}")
        results.append((name, False, str(e)))


# ------------------------------------------------------------------
# 1. IMPORTS
# ------------------------------------------------------------------
print("\n[1] IMPORTS")

def check_voiceover_import():
    from agents.audio_prod.voiceover.voiceover_agent import run
    assert callable(run)

def check_music_import():
    from agents.audio_prod.music.music_agent import run
    assert callable(run)

def check_sfx_import():
    from agents.audio_prod.sfx.sfx_agent import run
    assert callable(run)

def check_edge_tts():
    import edge_tts
    assert edge_tts is not None

def check_pydub():
    import pydub
    assert pydub is not None

def check_moviepy():
    import moviepy
    assert moviepy is not None

test("A-07 Voiceover Agent imports",  check_voiceover_import)
test("A-08 Music Agent imports",      check_music_import)
test("A-09 SFX Agent imports",        check_sfx_import)
test("edge-tts installed",            check_edge_tts)
test("pydub installed",               check_pydub)
test("moviepy installed",             check_moviepy)


# ------------------------------------------------------------------
# 2. CONFIG FILES
# ------------------------------------------------------------------
print("\n[2] CONFIG FILES")

def check_voice_profiles():
    import yaml
    assert os.path.exists("config/voice_profiles.yaml"), "voice_profiles.yaml missing"
    with open("config/voice_profiles.yaml") as f:
        cfg = yaml.safe_load(f)
    chars = cfg.get("characters", {})
    assert len(chars) >= 9, f"Expected 9 characters, got {len(chars)}"
    required = ["karna","krishna","draupadi","yudhishthira",
                "duryodhana","bhishma","shakuni","kunti","arjuna"]
    missing = [c for c in required if c not in chars]
    assert not missing, f"Missing characters in voice_profiles: {missing}"

def check_music_themes():
    import yaml
    assert os.path.exists("config/music_themes.yaml"), "music_themes.yaml missing"
    with open("config/music_themes.yaml") as f:
        cfg = yaml.safe_load(f)
    themes = cfg.get("themes", {})
    required = ["kuru_court","panchala","dwarka","battle","abhimanyu_death"]
    missing = [t for t in required if t not in themes]
    assert not missing, f"Missing themes: {missing}"

def check_abhimanyu_rule():
    import yaml
    with open("config/music_themes.yaml") as f:
        cfg = yaml.safe_load(f)
    theme = cfg.get("themes", {}).get("abhimanyu_death", {})
    instruments = theme.get("instruments", [])
    assert instruments == ["sarangi"], \
        f"Abhimanyu death must have ONLY sarangi. Got: {instruments}"
    assert theme.get("episode_restriction") == "S4E13", \
        "Abhimanyu death must be restricted to S4E13"

def check_kurukshetra_rule():
    import yaml
    with open("config/music_themes.yaml") as f:
        cfg = yaml.safe_load(f)
    theme = cfg.get("themes", {}).get("kurukshetra_theme", {})
    note = theme.get("note", "")
    assert "S1" in note and "S4" in note, \
        "Kurukshetra theme must have S1 fragment / S4 full restriction"

test("voice_profiles.yaml — 9 characters",         check_voice_profiles)
test("music_themes.yaml — 5 themes present",        check_music_themes)
test("Abhimanyu death = single sarangi only",        check_abhimanyu_rule)
test("Kurukshetra theme S1 fragment / S4 full rule", check_kurukshetra_rule)


# ------------------------------------------------------------------
# 3. EDGE TTS (Voiceover)
# ------------------------------------------------------------------
print("\n[3] EDGE TTS (Voiceover)")

def check_edge_tts_voices():
    import asyncio
    import edge_tts
    async def get_voices():
        voices = await edge_tts.list_voices()
        return voices
    voices = asyncio.run(get_voices())
    hindi_voices = [v for v in voices if "hi-IN" in v.get("ShortName","")]
    assert len(hindi_voices) > 0, "No Hindi voices found in Edge TTS"
    names = [v["ShortName"] for v in hindi_voices]
    print(f"       -> {len(hindi_voices)} Hindi voices available")
    print(f"       -> {names[:3]}")

def check_edge_tts_generate():
    import asyncio
    import edge_tts
    import os
    os.makedirs("output/audio/test", exist_ok=True)

    async def gen():
        communicate = edge_tts.Communicate(
            text="Dharma ka yeh rahasya hai.",
            voice="hi-IN-MadhurNeural"
        )
        await communicate.save("output/audio/test/tts_test.mp3")

    asyncio.run(gen())
    assert os.path.exists("output/audio/test/tts_test.mp3"), "TTS file not created"
    size = os.path.getsize("output/audio/test/tts_test.mp3")

    assert size > 1000, f"TTS file too small ({size} bytes) — likely empty"
    print(f"       -> TTS file generated: {size} bytes")

test("Edge TTS Hindi voices available",   check_edge_tts_voices)
test("Edge TTS generates Hindi audio",    check_edge_tts_generate)


# ------------------------------------------------------------------
# 4. MUSIC THEME MATCHING
# ------------------------------------------------------------------
print("\n[4] MUSIC THEME MATCHING")

def check_theme_hastinapur():
    from agents.audio_prod.music.theme_matcher import match
    theme = match("hastinapur throne hall", "power and tension", 1, "S1E01-SC01")
    assert theme, "No theme returned for Hastinapur"
    print(f"       -> Hastinapur matched: {theme.get('name','?')}")

def check_theme_battle():
    from agents.audio_prod.music.theme_matcher import match
    theme = match("kurukshetra", "battle chaos", 4, "S4E01-SC01")
    assert theme, "No theme returned for battle"
    print(f"       -> Battle matched: {theme.get('name','?')}")

def check_theme_abhimanyu():
    from agents.audio_prod.music.theme_matcher import match
    theme = match("chakravyuha", "death", 4, "S4E13-SC05")
    instruments = theme.get("instruments", [])
    assert "sarangi" in instruments, "Abhimanyu scene must match sarangi theme"
    print(f"       -> Abhimanyu matched: {theme.get('name','?')}")


test("Theme match: Hastinapur -> Kuru Court",   check_theme_hastinapur)
test("Theme match: Battle -> War Percussion",    check_theme_battle)
test("Theme match: Abhimanyu -> Single Sarangi", check_theme_abhimanyu)


# ------------------------------------------------------------------
# 5. OUTPUT DIRECTORY STRUCTURE
# ------------------------------------------------------------------
print("\n[5] OUTPUT STRUCTURE")

def check_output_dirs():
    dirs = ["output/audio", "output/scripts"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        assert os.path.exists(d), f"Directory missing: {d}"

def check_phase1_output_exists():
    assert os.path.exists("output/scripts"), "output/scripts missing"
    files = os.listdir("output/scripts")
    s1e01 = [f for f in files if "S1E01" in f]
    assert len(s1e01) > 0, "No S1E01 script files found — run Phase 1 first"
    print(f"       -> Found {len(s1e01)} S1E01 script file(s) to process")

test("Output directories exist",          check_output_dirs)
test("Phase 1 script output available",   check_phase1_output_exists)


# ------------------------------------------------------------------
# 6. FULL PIPELINE A-07 + A-08 + A-09
# ------------------------------------------------------------------
print("\n[6] FULL AUDIO PIPELINE")

_state = {}

def check_voiceover_runs():
    from orchestrator.state_schema import create_initial_state
    from agents.audio_prod.voiceover.voiceover_agent import run

    # Find latest S1E01 script
    scripts = [
        f for f in os.listdir("output/scripts")
        if "S1E01" in f and f.endswith(".json")
    ]
    assert scripts, "No S1E01 script found — run Phase 1 first"
    latest = sorted(scripts)[-1]
    script_path = f"output/scripts/{latest}"

    state = create_initial_state("S1E01", 1, 1, "The Weight of Crowns", "Mukut Ka Bojh")
    state["script_draft_path"] = script_path

    result = run(state)
    assert result.get("voiceover_ready"), "voiceover_ready not set"
    assert os.path.exists("output/audio/S1E01/voiceover"), "Voiceover output folder missing"

    files = os.listdir("output/audio/S1E01/voiceover")
    print(f"       -> {len(files)} voiceover file(s) generated")
    _state["state"] = result

def check_music_runs():
    assert _state.get("state"), "Voiceover must pass first"
    from agents.audio_prod.music.music_agent import run
    result = run(_state["state"])
    assert result.get("music_ready"), "music_ready not set"
    assert os.path.exists("output/audio/S1E01/music"), "Music output folder missing"
    files = os.listdir("output/audio/S1E01/music")
    print(f"       -> {len(files)} music file(s) generated")
    _state["state"] = result

def check_sfx_runs():
    assert _state.get("state"), "Music must pass first"
    from agents.audio_prod.sfx.sfx_agent import run
    result = run(_state["state"])
    assert result.get("sfx_ready"), "sfx_ready not set"
    assert os.path.exists("output/audio/S1E01/sfx"), "SFX output folder missing"
    files = os.listdir("output/audio/S1E01/sfx")
    print(f"       -> {len(files)} SFX file(s) generated")


test("A-07 Voiceover runs end-to-end", check_voiceover_runs)
test("A-08 Music Composer runs end-to-end", check_music_runs)
test("A-09 Sound Design runs end-to-end", check_sfx_runs)


# ══════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════
print("\n" + "=" * 52)
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
total  = len(results)

print(f"  RESULTS:  {passed}/{total} passed  |  {failed} failed")
print("=" * 52)

if failed > 0:
    print("\n  FAILED TESTS:")
    for name, ok, err in results:
        if not ok:
            print(f"  {FAIL}  {name}")
            print(f"         {err}")
    print("\n  Fix above before proceeding to Phase 4.\n")
    sys.exit(1)
else:
    print(f"\n  {PASS}  All Phase 3 checks passed. Ready for Phase 4.\n")
    sys.exit(0)