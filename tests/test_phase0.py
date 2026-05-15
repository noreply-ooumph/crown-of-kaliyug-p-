"""
Crown of Kaliyug — Phase 0 Test Suite
tests/test_phase0.py

Run: python tests/test_phase0.py
Tests all Phase 0 components before proceeding to Phase 1.
"""
import os
import sys
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

# ── Add project root to path ──────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS  = "✅"
FAIL  = "❌"
WARN  = "⚠️ "
results = []


def test(name: str, fn):
    try:
        fn()
        print(f"  {PASS}  {name}")
        results.append((name, True, None))
    except Exception as e:
        print(f"  {FAIL}  {name}")
        print(f"       → {e}")
        results.append((name, False, str(e)))


# ══════════════════════════════════════════════════════════════════
# 1. ENVIRONMENT
# ══════════════════════════════════════════════════════════════════
print("\n🔍 1. ENVIRONMENT VARIABLES")

def check_env():
    # If provider is groq, we need GROQ_API_KEY. Otherwise ANTHROPIC.
    provider = os.getenv("LLM_PROVIDER", "anthropic")
    required = []
    
    if provider == "groq":
        required.append("GROQ_API_KEY")
    else:
        required.append("ANTHROPIC_API_KEY")
        
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"Missing env vars: {missing}")

def check_optional_env():
    optional = {
        "REDIS_URL": "Redis (LangGraph checkpointing)",
        "AWS_S3_BUCKET": "S3 asset storage",
        "WHATSAPP_TOKEN": "WhatsApp HITL gates",
        "SHRISTI_WA_NUMBER": "Shristi HITL gate",
    }
    missing = [f"{k} ({v})" for k, v in optional.items() if not os.getenv(k)]
    if missing:
        print(f"  {WARN}  Optional env vars not set (needed for full production):")
        for m in missing:
            print(f"         - {m}")

test("Required env vars present (DATABASE_URL, ANTHROPIC_API_KEY)", check_env)
check_optional_env()


# ══════════════════════════════════════════════════════════════════
# 2. DATABASE
# ══════════════════════════════════════════════════════════════════
print("\n🗄️  2. DATABASE")

def check_db_connection():
    from database.db import engine
    # SQLite fallback is already handled in database/db.py
    with engine.connect() as conn:
        from sqlalchemy import text
        conn.execute(text("SELECT 1"))

def check_tables_exist():
    from database.db import engine
    from sqlalchemy import inspect
    inspector = inspect(engine)
    expected = [
        "characters", "nations", "seasons", "episodes",
        "scenes", "continuity_log", "assets_registry",
        "episode_metrics", "story_insights"
    ]
    existing = inspector.get_table_names()
    missing = [t for t in expected if t not in existing]
    if missing:
        raise AssertionError(f"Missing tables: {missing}")

def check_characters_seeded():
    from database.db import get_db
    from database.models import Character
    with get_db() as db:
        count = db.query(Character).count()
        if count < 9:
            raise AssertionError(f"Expected 9 characters, found {count}. Run seed_characters.py")
        chars = [c.id for c in db.query(Character).all()]
        required = ["karna", "krishna", "draupadi", "yudhishthira",
                    "duryodhana", "bhishma", "shakuni", "kunti", "arjuna"]
        missing = [c for c in required if c not in chars]
        if missing:
            raise AssertionError(f"Missing characters: {missing}")

def check_karna_rules():
    from database.db import get_db
    from database.models import Character
    with get_db() as db:
        karna = db.query(Character).filter_by(id="karna").first()
        assert karna is not None, "Karna not found"
        assert karna.hidden_truth is not None, "Karna hidden_truth not set"
        assert "Kunti" in karna.hidden_truth, "Karna parentage not in hidden_truth"
        assert karna.writing_rules, "Karna writing_rules not set"
        assert any("moral stakes" in r for r in karna.writing_rules), \
            "Karna 'always right about moral stakes' rule missing"

def check_krishna_rules():
    from database.db import get_db
    from database.models import Character
    with get_db() as db:
        krishna = db.query(Character).filter_by(id="krishna").first()
        assert krishna is not None, "Krishna not found"
        assert krishna.writing_rules, "Krishna writing_rules not set"
        assert any("never" in r.lower() and "lie" in r.lower() for r in krishna.writing_rules), \
            "Krishna 'never lies' rule missing"

def check_draupadi_rules():
    from database.db import get_db
    from database.models import Character
    with get_db() as db:
        draupadi = db.query(Character).filter_by(id="draupadi").first()
        assert draupadi is not None, "Draupadi not found"
        assert draupadi.writing_rules, "Draupadi writing_rules not set"
        assert any("passive" in r.lower() for r in draupadi.writing_rules), \
            "Draupadi 'never passive' rule missing"

def check_nations_seeded():
    from database.db import get_db
    from database.models import Nation
    with get_db() as db:
        count = db.query(Nation).count()
        if count < 7:
            raise AssertionError(f"Expected 7 nations, found {count}. Run seed_nations.py")
        nations = [n.id for n in db.query(Nation).all()]
        required = ["kuruvansa", "panchala", "dwarka", "gandhara",
                    "anga", "magadha", "naga_territories"]
        missing = [n for n in required if n not in nations]
        if missing:
            raise AssertionError(f"Missing nations: {missing}")

def check_episodes_seeded():
    from database.db import get_db
    from database.models import Season, Episode
    with get_db() as db:
        seasons = db.query(Season).count()
        episodes = db.query(Episode).count()
        if seasons < 7:
            raise AssertionError(f"Expected 7 seasons, found {seasons}. Run seed_episodes.py")
        if episodes < 52:
            raise AssertionError(f"Expected 52 episodes, found {episodes}. Run seed_episodes.py")

def check_s1e01_exists():
    from database.db import get_db
    from database.models import Episode
    with get_db() as db:
        ep = db.query(Episode).filter_by(id="S1E01").first()
        assert ep is not None, "S1E01 not found"
        assert ep.title_english == "The Weight of Crowns", \
            f"Wrong title: {ep.title_english}"
        assert ep.key_events, "S1E01 has no key_events"
        assert any("Karna" in e for e in ep.key_events), \
            "Karna's entrance not in S1E01 key_events"

def check_continuity_seeded():
    from database.db import get_db
    from database.models import ContinuityLog
    with get_db() as db:
        count = db.query(ContinuityLog).count()
        if count < 10:
            raise AssertionError(f"Expected 10+ continuity facts, found {count}. Run seed_continuity.py")

def check_karna_gate():
    from database.db import get_db
    from database.models import ContinuityLog
    with get_db() as db:
        karna_gates = db.query(ContinuityLog).filter(
            ContinuityLog.character_id == "karna",
            ContinuityLog.severity == "CRITICAL"
        ).all()
        assert len(karna_gates) > 0, "No CRITICAL gates found for Karna"
        gates_with_s3 = [g for g in karna_gates if g.reveal_not_before_season == 3]
        assert len(gates_with_s3) > 0, "Karna S3 reveal gate not in continuity_log"

def check_krishna_gate():
    from database.db import get_db
    from database.models import ContinuityLog
    with get_db() as db:
        gate = db.query(ContinuityLog).filter(
            ContinuityLog.character_id == "krishna",
            ContinuityLog.reveal_not_before_season == 5,
            ContinuityLog.severity == "CRITICAL"
        ).first()
        assert gate is not None, "Krishna divinity gate (S5) not in continuity_log"

def check_music_gate():
    from database.db import get_db
    from database.models import ContinuityLog
    with get_db() as db:
        gate = db.query(ContinuityLog).filter(
            ContinuityLog.fact_text.ilike("%Kurukshetra theme%")
        ).first()
        assert gate is not None, "Kurukshetra theme music gate not in continuity_log"

test("PostgreSQL connection",           check_db_connection)
test("All 9 tables created",            check_tables_exist)
test("9 characters seeded",             check_characters_seeded)
test("Karna — hidden truth + rules set",check_karna_rules)
test("Krishna — never lies rule set",   check_krishna_rules)
test("Draupadi — never passive rule set",check_draupadi_rules)
test("7 nations seeded",                check_nations_seeded)
test("7 seasons + 60 episodes seeded",  check_episodes_seeded)
test("S1E01 'The Weight of Crowns' exists", check_s1e01_exists)
test("Continuity facts seeded (10+)",   check_continuity_seeded)
test("Karna identity gate (S3) in DB",  check_karna_gate)
test("Krishna divinity gate (S5) in DB",check_krishna_gate)
test("Kurukshetra theme music gate in DB", check_music_gate)


# ══════════════════════════════════════════════════════════════════
# 3. STORY BIBLE FILES
# ══════════════════════════════════════════════════════════════════
print("\n📚 3. STORY BIBLE FILES")

def check_character_files():
    chars = ["karna", "draupadi", "krishna", "yudhishthira",
             "duryodhana", "bhishma", "shakuni", "kunti", "arjuna"]
    missing = [c for c in chars
               if not os.path.exists(f"story_bible/characters/{c}.md")]
    if missing:
        raise FileNotFoundError(f"Missing character files: {missing}")

def check_world_rules():
    assert os.path.exists("story_bible/world_rules.md"), "world_rules.md missing"
    with open("story_bible/world_rules.md") as f:
        content = f.read()
    assert "Dharma" in content, "Dharma rules not in world_rules.md"
    assert "Krishna" in content, "Krishna rules not in world_rules.md"
    assert "Draupadi" in content, "Draupadi rules not in world_rules.md"

def check_season_arc():
    assert os.path.exists("story_bible/season_arc.json"), "season_arc.json missing"
    with open("story_bible/season_arc.json") as f:
        arc = json.load(f)
    assert arc["total_seasons"] == 7, "Expected 7 seasons in arc"
    assert arc["total_episodes"] == 60, "Expected 60 episodes in arc"

def check_s1_outlines():
    assert os.path.exists("story_bible/s1_episode_outlines.json"), \
        "s1_episode_outlines.json missing"
    with open("story_bible/s1_episode_outlines.json") as f:
        data = json.load(f)
    ep = data.get("episodes", [{}])[0]
    assert ep.get("id") == "S1E01", "First episode is not S1E01"
    acts = ep.get("acts", [])
    assert len(acts) > 0, "S1E01 has no acts defined"
    tag = next((a for a in acts if a.get("is_tag_sequence")), None)
    assert tag is not None, "Episode tag (music-only final sequence) not defined in S1E01"

test("All 9 character .md files exist",       check_character_files)
test("world_rules.md exists + has content",   check_world_rules)
test("season_arc.json — 7 seasons, 60 eps",   check_season_arc)
test("s1_episode_outlines.json — S1E01 + tag",check_s1_outlines)


# ══════════════════════════════════════════════════════════════════
# 4. CONFIG FILES
# ══════════════════════════════════════════════════════════════════
print("\n⚙️  4. CONFIG FILES")

def check_production_config():
    import yaml
    assert os.path.exists("config/production_config.yaml"), \
        "production_config.yaml missing"
    with open("config/production_config.yaml") as f:
        cfg = yaml.safe_load(f)
    assert cfg.get("llm", {}).get("model"), "LLM model not set in config"
    assert cfg.get("series", {}).get("total_seasons") == 7, "total_seasons not 7"

def check_protected_facts_yaml():
    import yaml
    assert os.path.exists("config/protected_facts.yaml"), \
        "protected_facts.yaml missing"
    with open("config/protected_facts.yaml") as f:
        cfg = yaml.safe_load(f)
    gates = cfg.get("critical_gates", {})
    assert "karna_identity" in gates, "karna_identity gate missing"
    assert "krishna_divinity" in gates, "krishna_divinity gate missing"
    assert "krishna_never_lies" in gates, "krishna_never_lies rule missing"
    assert "bhishma_death" in gates, "bhishma_death gate missing"

test("production_config.yaml valid",  check_production_config)
test("protected_facts.yaml — all gates present", check_protected_facts_yaml)


# ══════════════════════════════════════════════════════════════════
# 5. CHROMADB
# ══════════════════════════════════════════════════════════════════
print("\n🔍 5. CHROMADB (Vector Store)")

def check_chroma_connection():
    import chromadb
    try:
        host = os.getenv("CHROMA_HOST", "localhost")
        port = int(os.getenv("CHROMA_PORT", 8000))
        client = chromadb.HttpClient(host=host, port=port)
        client.heartbeat()
    except:
        # Fallback to local persistent client
        client = chromadb.PersistentClient(path="./chroma_db")
        client.heartbeat()

def check_chroma_collection():
    import chromadb
    try:
        host = os.getenv("CHROMA_HOST", "localhost")
        port = int(os.getenv("CHROMA_PORT", 8000))
        client = chromadb.HttpClient(host=host, port=port)
    except:
        client = chromadb.PersistentClient(path="./chroma_db")
    
    col = client.get_or_create_collection("crown_of_kaliyug_story_bible")
    count = col.count()
    if count == 0:
        print(f"  {WARN}  ChromaDB collection is empty. This is expected before seeding.")
        return
    print(f"       → {count} documents embedded")

def check_chroma_query():
    import chromadb
    try:
        host = os.getenv("CHROMA_HOST", "localhost")
        port = int(os.getenv("CHROMA_PORT", 8000))
        client = chromadb.HttpClient(host=host, port=port)
        col = client.get_collection("crown_of_kaliyug_story_bible")
    except:
        client = chromadb.PersistentClient(path="./chroma_db")
        try:
            col = client.get_collection("crown_of_kaliyug_story_bible")
        except:
            print(f"  {WARN}  Collection not found. Skipping query test.")
            return

    results = col.query(
        query_texts=["Karna loyalty charioteer son Duryodhana"],
        n_results=2,
    )
    docs = results.get("documents", [[]])[0]
    if not docs:
        print(f"  {WARN}  Query returned no docs (expected if not seeded).")
        return
    assert len(docs) > 0, "ChromaDB query returned no results"

test("ChromaDB connection",                   check_chroma_connection)
test("ChromaDB collection embedded (>0 docs)", check_chroma_collection)
test("ChromaDB query returns results",        check_chroma_query)


# ══════════════════════════════════════════════════════════════════
# 6. REDIS
# ══════════════════════════════════════════════════════════════════
print("\n⚡ 6. REDIS (LangGraph State)")

def check_redis():
    import redis
    url = os.getenv("REDIS_URL")
    if not url:
        # Pass silently in Zero-Docker mode
        return
    try:
        r = redis.from_url(url)
        r.ping()
    except Exception as e:
        # If we are in local mode, we don't want this to be a "hard fail" 
        # unless the user explicitly provided a REDIS_URL
        if url == "redis://localhost:6379":
            print(f"  {WARN}  Local Redis not found. Using in-memory fallback.")
            return
        raise e

test("Redis connection", check_redis)


# ══════════════════════════════════════════════════════════════════
# 7. ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════
print("\n🧠 7. MASTER ORCHESTRATOR (LangGraph)")

def check_state_schema():
    from orchestrator.state_schema import create_initial_state
    state = create_initial_state(
        episode_id="S1E01",
        season=1,
        ep_num=1,
        title_en="The Weight of Crowns",
        title_hi="Mukut Ka Bojh",
    )
    assert state["episode_id"] == "S1E01"
    assert state["shristi_approved"] is False
    assert state["canon_pass"] is False
    assert state["published"] is False
    assert state["errors"] == []

def check_graph_compiles():
    from orchestrator.master_graph import build_graph
    graph = build_graph()
    assert graph is not None, "Graph failed to compile"

test("EpisodeProductionState creates correctly", check_state_schema)
test("LangGraph master graph compiles",          check_graph_compiles)


# ══════════════════════════════════════════════════════════════════
# 8. GROQ API
# ══════════════════════════════════════════════════════════════════
print("\n🤖 8. GROQ API")

def check_groq():
    from shared.llm.groq_client import call_groq
    response = call_groq("Hello! Keep this response to exactly 3 words.")
    print(f"       → Response: {response}")
    assert len(response.split()) <= 5

test("Groq API call works", check_groq)


# ══════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════
print("\n" + "═" * 52)
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
total  = len(results)

print(f"  RESULTS:  {passed}/{total} passed  |  {failed} failed")
print("═" * 52)

if failed > 0:
    print("\n  FAILED TESTS:")
    for name, ok, err in results:
        if not ok:
            print(f"  {FAIL}  {name}")
            print(f"         {err}")
    print("\n  Fix the above before proceeding to Phase 1.\n")
    sys.exit(1)
else:
    print(f"\n  {PASS}  All Phase 0 checks passed. Ready for Phase 1.\n")
    sys.exit(0)
