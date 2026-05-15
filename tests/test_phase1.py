"""
Crown of Kaliyug - Phase 1 Test Suite
tests/test_phase1.py

Run: python tests/test_phase1.py
Tests all Phase 1 components: A-02, A-03, A-04
"""
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


PASS = "[PASS]"
FAIL = "[FAIL]"
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



def check_llm_client():
    from shared.llm.llm_client import call_llm, call_llm_json
    assert callable(call_llm)
    assert callable(call_llm_json)

def check_rag_retriever():
    from agents.story_engine.script_writer.rag_retriever import retrieve_context
    assert callable(retrieve_context)

def check_scene_generator():
    from agents.story_engine.script_writer.scene_generator import generate_script, _normalize
    assert callable(generate_script)
    assert callable(_normalize)

def check_teaser_cutter():
    from agents.story_engine.script_writer.teaser_cutter import generate_teasers
    assert callable(generate_teasers)

def check_script_writer_agent():
    from agents.story_engine.script_writer.script_writer_agent import run
    assert callable(run)

def check_dialogue_imports():
    from agents.story_engine.dialogue.dialogue_agent import run
    from agents.story_engine.dialogue.character_loader import load_character_prompt
    from agents.story_engine.dialogue.emotion_tagger import validate_tag, get_voice_settings
    assert callable(run)
    assert callable(load_character_prompt)
    assert callable(validate_tag)

def check_canon_imports():
    from agents.story_engine.canon_guardian.canon_guardian_agent import run
    from agents.story_engine.canon_guardian.fact_checker import check_script
    from agents.story_engine.canon_guardian.continuity_updater import extract_and_save
    from agents.story_engine.canon_guardian.violation_reporter import format_violations
    assert callable(run)

test("LLM client imports",          check_llm_client)
test("RAG retriever imports",        check_rag_retriever)
test("Scene generator imports",      check_scene_generator)
test("Teaser cutter imports",        check_teaser_cutter)
test("Script Writer agent imports",  check_script_writer_agent)
test("Dialogue Agent imports",       check_dialogue_imports)
test("Canon Guardian imports",       check_canon_imports)


# ------------------------------------------------------------------
# 2. PROMPT FILES
# ------------------------------------------------------------------
print("\n[2] PROMPT FILES")

def check_script_writer_prompt():
    assert os.path.exists("prompts/script_writer_system.txt"), "script_writer_system.txt missing"
    with open("prompts/script_writer_system.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 100, "script_writer_system.txt is empty"
    assert "dharma" in content.lower() or "scene" in content.lower(), \
        "script_writer_system.txt missing key content"

def check_dialogue_prompts():
    chars = ["krishna","karna","draupadi","duryodhana","bhishma",
             "shakuni","yudhishthira","kunti","arjuna"]
    missing = [c for c in chars if not os.path.exists(f"prompts/dialogue_{c}.txt")]
    if missing:
        raise FileNotFoundError(f"Missing dialogue prompts: {missing}")
    for c in chars:
        with open(f"prompts/dialogue_{c}.txt", "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 50, f"dialogue_{c}.txt is empty"


def check_prompt_content():
    from agents.story_engine.dialogue.character_loader import load_character_prompt
    for char in ["krishna", "karna", "draupadi"]:
        prompt = load_character_prompt(char)
        assert len(prompt) > 100, f"{char} prompt too short"
        assert "JSON" in prompt, f"{char} prompt missing JSON instruction"

test("script_writer_system.txt exists + has content", check_script_writer_prompt)
test("All 9 dialogue prompt files exist",              check_dialogue_prompts)
test("Dialogue prompts load correctly via loader",     check_prompt_content)


# ------------------------------------------------------------------
# 3. EMOTION TAGGER
# ------------------------------------------------------------------
print("\n[3] EMOTION TAGGER")

def check_valid_tags():
    from agents.story_engine.dialogue.emotion_tagger import validate_tag
    assert validate_tag("[formal]")    == "[formal]"
    assert validate_tag("[warm]")      == "[warm]"
    assert validate_tag("[invalid]")   == "[formal]"
    assert validate_tag("no_brackets") == "[formal]"

def check_voice_settings():
    from agents.story_engine.dialogue.emotion_tagger import get_voice_settings
    settings = get_voice_settings("[rage]")
    assert "stability" in settings
    assert settings["stability"] < 0.5, "Roar/Rage should have low stability"

    settings2 = get_voice_settings("[quiet]")
    assert settings2["stability"] > 0.9, "Quiet/Whisper should have high stability"

def check_tag_extraction():
    from agents.story_engine.dialogue.emotion_tagger import extract_tag_from_line
    text, tag = extract_tag_from_line("I challenge you. [formal]")
    assert text == "I challenge you."
    assert tag  == "[formal]"

    text2, tag2 = extract_tag_from_line("No tag here at all")
    assert tag2 == "[formal]"

test("validate_tag works correctly",         check_valid_tags)
test("voice settings map to ElevenLabs",     check_voice_settings)
test("extract_tag_from_line works",          check_tag_extraction)


# ------------------------------------------------------------------
# 4. NORMALIZE FUNCTION
# ------------------------------------------------------------------
print("\n[4] SCENE NORMALIZER")

def check_normalize_script_key():
    from agents.story_engine.script_writer.scene_generator import _normalize
    raw = {
        "script": [
            {"scene": 1, "location": "Hastinapur", "description": "Tournament begins",
             "characters": ["Arjuna", "Karna"], "dialogue": [
                {"character": "Karna", "line": "I challenge you."}
             ]}
        ]
    }
    result = _normalize(raw, "S1E01")
    assert len(result["scenes"]) == 1, "Expected 1 scene"
    assert result["scenes"][0]["location"] == "Hastinapur"
    assert result["total_scenes"] == 1

def check_normalize_scenes_key():
    from agents.story_engine.script_writer.scene_generator import _normalize
    raw = {
        "scenes": [
            {"scene_id": "S1E01-SC01", "location": "Palace", "action_lines": ["Drums beat."],
             "characters_present": ["Bhishma"], "dialogue_slots": []}
        ]
    }
    result = _normalize(raw, "S1E01")
    assert len(result["scenes"]) == 1

def check_normalize_dialogue_slots():
    from agents.story_engine.script_writer.scene_generator import _normalize
    raw = {
        "script": [
            {"scene": 1, "location": "Court", "description": "Tense exchange",
             "characters": ["Krishna"], "dialogue": [
                {"character": "Krishna", "line": "What is it you are really asking?"},
                {"character": "Arjuna",  "line": "I do not know."}
             ]}
        ]
    }
    result = _normalize(raw, "S1E01")
    slots = result["scenes"][0]["dialogue_slots"]
    assert len(slots) == 2, f"Expected 2 slots, got {len(slots)}"
    assert slots[0]["character"] == "krishna"
    assert slots[0]["text"] == "What is it you are really asking?"
    assert slots[0]["slot_id"] == "S1E01-SC01-L01"

test("Normalize handles 'script' key",    check_normalize_script_key)
test("Normalize handles 'scenes' key",    check_normalize_scenes_key)
test("Normalize converts dialogue slots", check_normalize_dialogue_slots)


# ------------------------------------------------------------------
# 5. RAG RETRIEVER
# ------------------------------------------------------------------
print("\n[5] RAG RETRIEVER")

def check_rag_retrieves_characters():
    from agents.story_engine.script_writer.rag_retriever import retrieve_context
    ctx = retrieve_context("S1E01", ["karna", "krishna"], 1)
    assert len(ctx) > 100, "RAG returned too little context"
    assert "KARNA" in ctx.upper() or "karna" in ctx.lower(), "Karna not in RAG context"

def check_rag_world_rules():
    from agents.story_engine.script_writer.rag_retriever import retrieve_context
    ctx = retrieve_context("S1E01", [], 1)
    assert "WORLD RULES" in ctx or "dharma" in ctx.lower() or "world" in ctx.lower(), \
        "World rules not retrieved"

def check_rag_continuity_facts():
    from agents.story_engine.script_writer.rag_retriever import retrieve_context
    ctx = retrieve_context("S1E01", ["karna"], 1)
    assert len(ctx) > 0, "RAG returned empty context"

test("RAG retrieves character profiles",  check_rag_retrieves_characters)
test("RAG retrieves world rules",         check_rag_world_rules)
test("RAG retrieves continuity facts",    check_rag_continuity_facts)


# ------------------------------------------------------------------
# 6. LLM CLIENT
# ------------------------------------------------------------------
print("\n[6] LLM CLIENT")

def check_llm_call():
    from shared.llm.llm_client import call_llm
    response = call_llm(
        system_prompt="Reply with exactly: PHASE_1_OK",
        user_message="Say the test word.",
        max_tokens=20,
    )
    assert "PHASE_1_OK" in response, f"Unexpected response: {response}"

def check_llm_json_call():
    from shared.llm.llm_client import call_llm_json
    result = call_llm_json(
        system_prompt="Return ONLY JSON with key 'status' set to 'ok'.",
        user_message="Return the JSON now.",
        max_tokens=50,
    )
    assert isinstance(result, dict), "Expected dict"
    assert result.get("status") == "ok", f"Unexpected result: {result}"

test("LLM call returns response",     check_llm_call)
test("LLM JSON call returns dict",    check_llm_json_call)


# ------------------------------------------------------------------
# 7. FULL PIPELINE -- A-02 + A-03 + A-04
# ------------------------------------------------------------------
print("\n[7] FULL PIPELINE (A-02 -> A-03 -> A-04)")

_pipeline_state = {}

def check_script_writer_runs():
    from orchestrator.state_schema import create_initial_state
    from agents.story_engine.script_writer.script_writer_agent import run
    state = create_initial_state("S1E01", 1, 1, "The Weight of Crowns", "Mukut Ka Bojh")
    result = run(state)
    assert result.get("script_draft_path"), "No script_draft_path in state"
    assert os.path.exists(result["script_draft_path"]), "Script file not created"
    with open(result["script_draft_path"]) as f:
        script = json.load(f)
    assert len(script.get("scenes", [])) > 0, "Script has 0 scenes"
    _pipeline_state["state"]  = result
    _pipeline_state["scenes"] = len(script["scenes"])
    print(f"       -> {_pipeline_state['scenes']} scenes generated")

def check_dialogue_agent_runs():
    assert _pipeline_state.get("state"), "Script Writer must pass first"
    print("       -> Sleeping 5s to avoid rate limits...")
    time.sleep(5)
    from agents.story_engine.dialogue.dialogue_agent import run
    state  = _pipeline_state["state"]
    result = run(state)
    assert result.get("script_draft_path"), "No script_draft_path after dialogue"
    assert os.path.exists(result["script_draft_path"]), "Dialogue script file not found"
    with open(result["script_draft_path"]) as f:
        script = json.load(f)
    assert "scenes" in script, "scenes key missing from dialogue output"
    _pipeline_state["state"] = result
    print(f"       -> Dialogue filled for {len(script['scenes'])} scenes")

def check_canon_guardian_structure():
    from agents.story_engine.canon_guardian.fact_checker import check_script
    assert _pipeline_state.get("state"), "Previous agents must pass first"
    print("       -> Sleeping 5s to avoid rate limits...")
    time.sleep(5)
    with open(_pipeline_state["state"]["script_draft_path"], "r", encoding="utf-8") as f:
        script = json.load(f)
    result = check_script(script, season=1)
    assert "status" in result, "Canon result missing 'status'"
    assert result["status"] in ["PASS", "FAIL"], f"Invalid status: {result['status']}"
    assert "violations" in result, "Canon result missing 'violations'"
    _pipeline_state["canon_result"] = result
    print(f"       -> Canon check: {result['status']} ({len(result.get('violations',[]))} violations)")

def check_output_files_exist():
    # Note: We check 'output/scripts' as requested by the user
    assert os.path.exists("output/scripts"), "output/scripts folder missing"
    files = os.listdir("output/scripts")
    s1e01_files = [f for f in files if "S1E01" in f]
    assert len(s1e01_files) > 0, "No S1E01 output files found"
    print(f"       -> {len(s1e01_files)} S1E01 output file(s) found")

test("A-02 Script Writer runs end-to-end",   check_script_writer_runs)
test("A-03 Dialogue Agent runs end-to-end",  check_dialogue_agent_runs)
test("A-04 Canon Guardian check runs",       check_canon_guardian_structure)
test("Output files created in output/",      check_output_files_exist)


# ------------------------------------------------------------------
# 8. SCHEMA VALIDATION
# ------------------------------------------------------------------
print("\n[8] SCHEMA VALIDATION")

def check_script_schema():
    assert os.path.exists("schemas/script_output.json"), "script_output.json missing"
    with open("schemas/script_output.json") as f:
        schema = json.load(f)
    assert "properties" in schema or "title" in schema, "Invalid schema"

def check_canon_schema():
    assert os.path.exists("schemas/canon_result.json"), "canon_result.json missing"
    with open("schemas/canon_result.json") as f:
        schema = json.load(f)
    assert "properties" in schema

test("script_output.json schema valid",  check_script_schema)
test("canon_result.json schema valid",   check_canon_schema)


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
    print("\n  Fix the above before proceeding to Phase 2.\n")
    sys.exit(1)
else:
    print(f"\n  {PASS}  All Phase 1 checks passed. Ready for Phase 2.\n")
    sys.exit(0)
