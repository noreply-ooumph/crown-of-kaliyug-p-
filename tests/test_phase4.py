"""
Crown of Kaliyug - Phase 4 Test Suite
tests/test_phase4.py

Run: python tests/test_phase4.py
Tests A-10 Video Editor + A-11 Platform Formatter
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS = "✅"
FAIL = "❌"
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


# ══════════════════════════════════════════════════════════════════
# 1. IMPORTS
# ══════════════════════════════════════════════════════════════════
print("\n📦 1. IMPORTS")

def check_editor_agent():
    from agents.post_prod.editor.agent import run
    assert callable(run)

def check_scene_sequencer():
    from agents.post_prod.editor.scene_sequencer import get_ordered_clips, validate_sequence
    assert callable(get_ordered_clips)
    assert callable(validate_sequence)

def check_audio_mixer():
    from agents.post_prod.editor.audio_mixer import mix_scene_audio
    assert callable(mix_scene_audio)

def check_tag_enforcer():
    from agents.post_prod.editor.tag_enforcer import enforce_tag_rules, validate_tag_clip, is_tag_scene
    assert callable(enforce_tag_rules)
    assert callable(validate_tag_clip)

def check_subtitle_gen():
    from agents.post_prod.editor.subtitle_gen import generate_subtitles
    assert callable(generate_subtitles)

def check_intro_outro():
    from agents.post_prod.editor.intro_outro import get_intro_clip, get_outro_clip, branding_status
    assert callable(branding_status)

def check_formatter_agent():
    from agents.post_prod.formatter.formatter_agent import run
    assert callable(run)

def check_platform_exporters():
    from agents.post_prod.formatter.youtube_export    import export
    from agents.post_prod.formatter.insta_reel_export import export
    from agents.post_prod.formatter.twitter_export    import export
    from agents.post_prod.formatter.wa_export         import export
    from agents.post_prod.formatter.thumbnail_gen     import generate

def check_moviepy():
    import moviepy
    assert moviepy is not None

def check_ffmpeg():
    import subprocess
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    assert result.returncode == 0, "ffmpeg not found"

test("A-10 editor agent imports",       check_editor_agent)
test("Scene sequencer imports",         check_scene_sequencer)
test("Audio mixer imports",             check_audio_mixer)
test("Tag enforcer imports",            check_tag_enforcer)
test("Subtitle generator imports",      check_subtitle_gen)
test("Intro/outro imports",             check_intro_outro)
test("A-11 formatter agent imports",    check_formatter_agent)
test("All platform exporters import",   check_platform_exporters)
test("moviepy installed",               check_moviepy)
test("ffmpeg installed",                check_ffmpeg)


# ══════════════════════════════════════════════════════════════════
# 2. TAG ENFORCER — Series Bible rules
# ══════════════════════════════════════════════════════════════════
print("\n🎬 2. TAG ENFORCER (Series Bible Rules)")

def check_tag_detection():
    from agents.post_prod.editor.tag_enforcer import is_tag_scene
    assert is_tag_scene({"is_tag_sequence": True})  == True
    assert is_tag_scene({"is_tag_sequence": False}) == False
    assert is_tag_scene({})                          == False

def check_tag_suppresses_voiceover():
    from agents.post_prod.editor.tag_enforcer import enforce_tag_rules
    scene      = {"scene_id": "S1E01-TAG", "is_tag_sequence": True}
    clip_cfg   = {"voiceover_enabled": True, "dialogue_enabled": True, "music_enabled": True}
    result     = enforce_tag_rules(scene, clip_cfg)
    assert result["voiceover_enabled"] == False, "Voiceover must be suppressed in tag"
    assert result["dialogue_enabled"]  == False, "Dialogue must be suppressed in tag"
    assert result["music_enabled"]     == True,  "Music must be ON in tag"
    assert result["tag_enforced"]      == True

def check_tag_8min_duration():
    from agents.post_prod.editor.tag_enforcer import enforce_tag_rules
    scene    = {"scene_id": "S1E01-TAG", "is_tag_sequence": True}
    clip_cfg = {}
    result   = enforce_tag_rules(scene, clip_cfg)
    assert result["target_duration"] == 480, "Tag must be 480 seconds (8 min)"

def check_normal_scene_not_affected():
    from agents.post_prod.editor.tag_enforcer import enforce_tag_rules
    scene    = {"scene_id": "S1E01-SC01", "is_tag_sequence": False}
    clip_cfg = {"voiceover_enabled": True, "dialogue_enabled": True}
    result   = enforce_tag_rules(scene, clip_cfg)
    assert result["voiceover_enabled"] == True, "Normal scene voiceover must not be suppressed"

def check_tag_validation():
    from agents.post_prod.editor.tag_enforcer import validate_tag_clip, enforce_tag_rules
    scene    = {"scene_id": "S1E01-TAG", "is_tag_sequence": True}
    clip_cfg = enforce_tag_rules(scene, {})
    assert validate_tag_clip(scene, clip_cfg) == True

test("Tag detection works",               check_tag_detection)
test("Tag suppresses voiceover (rule)",   check_tag_suppresses_voiceover)
test("Tag = 480 sec / 8 min (rule)",      check_tag_8min_duration)
test("Normal scene not affected",         check_normal_scene_not_affected)
test("Tag validation passes",             check_tag_validation)


# ══════════════════════════════════════════════════════════════════
# 3. SCENE SEQUENCER
# ══════════════════════════════════════════════════════════════════
print("\n🎞️  3. SCENE SEQUENCER")

def check_sequencer_ordering():
    from agents.post_prod.editor.scene_sequencer import get_ordered_clips
    scenes = [
        {"scene_id": "S1E01-SC03", "scene_number": 3, "is_tag_sequence": False, "location": "Arena"},
        {"scene_id": "S1E01-SC01", "scene_number": 1, "is_tag_sequence": False, "location": "Arena"},
        {"scene_id": "S1E01-SC02", "scene_number": 2, "is_tag_sequence": False, "location": "Arena"},
        {"scene_id": "S1E01-TAG",  "scene_number": 99,"is_tag_sequence": True,  "location": "Multiple"},
    ]
    clips = get_ordered_clips("S1E01", scenes)
    assert clips[0]["scene_id"] == "S1E01-SC01", "SC01 must be first"
    assert clips[-1]["scene_id"] == "S1E01-TAG",  "Tag must be last"
    print(f"       -> {len(clips)} clips ordered correctly")

def check_sequencer_tag_last():
    from agents.post_prod.editor.scene_sequencer import get_ordered_clips
    scenes = [
        {"scene_id": "S1E01-TAG",  "scene_number": 99, "is_tag_sequence": True,  "location": ""},
        {"scene_id": "S1E01-SC01", "scene_number": 1,  "is_tag_sequence": False, "location": ""},
    ]
    clips = get_ordered_clips("S1E01", scenes)
    tag_clips = [c for c in clips if c["is_tag"]]
    assert len(tag_clips) == 1
    assert clips[-1]["is_tag"] == True, "Tag sequence must be last"

def check_validate_sequence_missing():
    from agents.post_prod.editor.scene_sequencer import validate_sequence
    clips = [
        {"scene_id": "SC01", "video_exists": False, "is_tag": False},
        {"scene_id": "SC02", "video_exists": False, "is_tag": False},
    ]
    result = validate_sequence(clips)
    assert result == False, "Should return False when clips missing"

test("Scene ordering correct",      check_sequencer_ordering)
test("Tag sequence always last",    check_sequencer_tag_last)
test("Validates missing clips",     check_validate_sequence_missing)


# ══════════════════════════════════════════════════════════════════
# 4. BRANDING / ASSETS
# ══════════════════════════════════════════════════════════════════
print("\n🎨 4. BRANDING ASSETS")

def check_branding_status():
    from agents.post_prod.editor.intro_outro import branding_status
    status = branding_status()
    assert "intro_bumper" in status
    assert "end_card" in status
    print(f"       -> Intro bumper: {status['intro_bumper']}")
    print(f"       -> End card:     {status['end_card']}")

def check_branding_folder():
    assert os.path.exists("assets/branding"), "assets/branding/ folder missing"

def check_platform_specs():
    assert os.path.exists("config/platform_specs.yaml"), "config/platform_specs.yaml missing"
    import yaml
    with open("config/platform_specs.yaml") as f:
        specs = yaml.safe_load(f)
    required = ["youtube", "instagram_reel", "twitter", "whatsapp"]
    missing  = [p for p in required if p not in specs]
    assert not missing, f"Missing platform specs: {missing}"
    print(f"       -> {len(specs)} platform specs loaded")

def check_subtitle_prompt():
    assert os.path.exists("prompts/subtitle_generator.txt"), "subtitle_generator.txt missing"
    with open("prompts/subtitle_generator.txt") as f:
        content = f.read()
    assert len(content) > 50, "subtitle_generator.txt is empty"

test("Branding status returns dict",  check_branding_status)
test("assets/branding/ folder exists", check_branding_folder)
test("platform_specs.yaml valid",     check_platform_specs)
test("subtitle_generator.txt exists", check_subtitle_prompt)


# ══════════════════════════════════════════════════════════════════
# 5. SUBTITLE GENERATOR
# ══════════════════════════════════════════════════════════════════
print("\n📝 5. SUBTITLE GENERATOR")

def check_srt_format():
    from agents.post_prod.editor.subtitle_gen import _fmt
    assert _fmt(0)      == "00:00:00,000"
    assert _fmt(61.5)   == "00:01:01,500"
    assert _fmt(3661.0) == "01:01:01,000"

def check_srt_from_script():
    from agents.post_prod.editor.subtitle_gen import generate_subtitles
    script_path = "output/scripts/S1E01_draft_1.json"
    if not os.path.exists(script_path):
        print(f"       -> Script not found — skipping SRT test")
        return
    result = generate_subtitles("S1E01_test", script_path)
    assert "hindi_srt" in result
    assert os.path.exists(result["hindi_srt"]), "Hindi SRT file not created"
    with open(result["hindi_srt"]) as f:
        content = f.read()
    print(f"       -> SRT generated: {len(content)} chars")

test("SRT timestamp format correct",  check_srt_format)
test("SRT generates from script",     check_srt_from_script)


# ══════════════════════════════════════════════════════════════════
# 6. FULL A-10 RUN (placeholder mode)
# ══════════════════════════════════════════════════════════════════
print("\n🎬 6. FULL A-10 RUN")

_state = {}

def check_a10_runs():
    from orchestrator.state_schema import create_initial_state
    from agents.post_prod.editor.agent import run

    script_path = "output/scripts/S1E01_draft_1.json"
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script not found: {script_path} — run Phase 1 first")

    state = create_initial_state("S1E01", 1, 1, "The Weight of Crowns", "Mukut Ka Bojh")
    state["script_draft_path"] = script_path
    result = run(state)

    assert result.get("video_editor_ready") == True, "video_editor_ready not set"
    assert result.get("master_video_path"),           "master_video_path not set"
    assert os.path.exists(result["master_video_path"]), "Output file not created"

    _state["result"] = result
    print(f"       -> Output: {result['master_video_path']}")

def check_assembly_plan_valid():
    if not _state.get("result"):
        raise Exception("A-10 must pass first")
    out_path = _state["result"]["master_video_path"]
    if out_path.endswith(".json"):
        with open(out_path) as f:
            plan = json.load(f)
        assert "episode_id" in plan
        assert "clips" in plan
        scenes = plan["clips"]
        assert len(scenes) > 0, "No scenes in assembly plan"
        print(f"       -> Assembly plan: {len(scenes)} scenes")
        for s in scenes[:3]:
            print(f"          {s['scene_id']:20} | {s['video_status']}")

test("A-10 runs end-to-end",          check_a10_runs)
test("Assembly plan JSON valid",       check_assembly_plan_valid)


# ══════════════════════════════════════════════════════════════════
# 7. FULL A-11 RUN (placeholder mode)
# ══════════════════════════════════════════════════════════════════
print("\n📱 7. FULL A-11 RUN")

def check_a11_placeholder():
    from orchestrator.state_schema import create_initial_state
    from agents.post_prod.formatter.formatter_agent import run

    state = create_initial_state("S1E01", 1, 1, "The Weight of Crowns", "Mukut Ka Bojh")
    state["master_video_path"]    = "output/final/S1E01_assembly_plan.json"
    state["priya_shelly_approved"] = False  # not approved yet

    result = run(state)
    assert result.get("formatter_ready") == False, "Should be False — approval pending"
    assert result.get("formatter_status") == "PENDING_APPROVAL"
    print(f"       -> Status: {result.get('formatter_status')}")
    print(f"       -> Approval request saved correctly")

def check_a11_output_structure():
    out_dir = "output/final"
    assert os.path.exists(out_dir), "output/final/ missing"
    files = os.listdir(out_dir)
    s1e01 = [f for f in files if "S1E01" in f]
    assert len(s1e01) > 0, "No S1E01 output files found"
    print(f"       -> {len(s1e01)} S1E01 output file(s) in output/final/")

test("A-11 waits for approval",        check_a11_placeholder)
test("output/final/ has files",       check_a11_output_structure)


# ══════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════
print("\n" + "="*52)
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
total  = len(results)
print(f"  RESULTS:  {passed}/{total} passed  |  {failed} failed")
print("="*52)

if failed > 0:
    print("\n  FAILED TESTS:")
    for name, ok, err in results:
        if not ok:
            print(f"  {FAIL}  {name}")
            print(f"         {err}")
    print("\n  Fix above before Phase 5.\n")
    sys.exit(1)
else:
    print(f"\n  {PASS}  All Phase 4 checks passed. Ready for Phase 5.\n")
    sys.exit(0)