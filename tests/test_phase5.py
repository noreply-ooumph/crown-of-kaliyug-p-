"""
Crown of Kaliyug - Phase 5 Test Suite
tests/test_phase5.py

Run: python tests/test_phase5.py
Tests A-12 Analytics Agent
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

def check_analytics_agent():
    from agents.analytics.analytics_agent import run
    assert callable(run)

def check_publishers():
    from agents.analytics.youtube_publisher  import publish as yt
    from agents.analytics.insta_publisher    import publish as ig
    from agents.analytics.twitter_publisher  import publish as tw
    assert callable(yt) and callable(ig) and callable(tw)

def check_metric_tracker():
    from agents.analytics.metric_tracker import fetch_metrics, track
    assert callable(fetch_metrics)
    assert callable(track)

def check_weekly_report():
    from agents.analytics.weekly_report import generate_report, generate
    assert callable(generate_report)
    assert callable(generate)

def check_story_intelligence():
    from agents.analytics.story_intelligence import analyze_sentiment, analyze
    assert callable(analyze_sentiment)
    assert callable(analyze)

def check_ab_tracker():
    from agents.analytics.ab_tracker import track_test, track_ab
    assert callable(track_test)
    assert callable(track_ab)

test("Analytics agent imports",     check_analytics_agent)
test("All 3 publishers import",     check_publishers)
test("Metric tracker imports",      check_metric_tracker)
test("Weekly report imports",       check_weekly_report)
test("Story intelligence imports",  check_story_intelligence)
test("A/B tracker imports",         check_ab_tracker)


# ══════════════════════════════════════════════════════════════════
# 2. PUBLISHER STUBS
# ══════════════════════════════════════════════════════════════════
print("\n📡 2. PUBLISHERS (API stub check)")

def check_youtube_no_crash():
    from agents.analytics.youtube_publisher import publish
    result = publish("S1E01", "output/final/S1E01_youtube.mp4", {})
    # Should not crash — returns None or stub response when no API key
    assert result is None or isinstance(result, (dict, str, bool))
    print(f"       -> YouTube publish stub: {type(result).__name__}")

def check_insta_no_crash():
    from agents.analytics.insta_publisher import publish
    result = publish("S1E01", "output/final/S1E01_instagram_reel.mp4", {})
    assert result is None or isinstance(result, (dict, str, bool))
    print(f"       -> Instagram publish stub: {type(result).__name__}")

def check_twitter_no_crash():
    from agents.analytics.twitter_publisher import publish
    result = publish("S1E01", "output/final/S1E01_twitter.mp4", {})
    assert result is None or isinstance(result, (dict, str, bool))
    print(f"       -> Twitter publish stub: {type(result).__name__}")

test("YouTube publisher no crash",   check_youtube_no_crash)
test("Instagram publisher no crash", check_insta_no_crash)
test("Twitter publisher no crash",   check_twitter_no_crash)


# ══════════════════════════════════════════════════════════════════
# 3. METRIC TRACKER
# ══════════════════════════════════════════════════════════════════
print("\n📊 3. METRIC TRACKER")

def check_fetch_metrics_no_crash():
    from agents.analytics.metric_tracker import fetch_metrics
    result = fetch_metrics("S1E01")
    assert result is None or isinstance(result, dict)
    print(f"       -> fetch_metrics stub: {type(result).__name__}")

def check_track_alias():
    from agents.analytics.metric_tracker import track, fetch_metrics
    assert track == fetch_metrics, "track must be alias for fetch_metrics"

test("fetch_metrics no crash",   check_fetch_metrics_no_crash)
test("track alias correct",      check_track_alias)


# ══════════════════════════════════════════════════════════════════
# 4. WEEKLY REPORT
# ══════════════════════════════════════════════════════════════════
print("\n📋 4. WEEKLY REPORT")

def check_weekly_report_no_crash():
    from agents.analytics.weekly_report import generate_report
    result = generate_report("S1E01")
    assert result is None or isinstance(result, (dict, str))
    print(f"       -> generate_report stub: {type(result).__name__}")

def check_generate_alias():
    from agents.analytics.weekly_report import generate, generate_report
    assert generate == generate_report

test("generate_report no crash",  check_weekly_report_no_crash)
test("generate alias correct",    check_generate_alias)


# ══════════════════════════════════════════════════════════════════
# 5. STORY INTELLIGENCE
# ══════════════════════════════════════════════════════════════════
print("\n🧠 5. STORY INTELLIGENCE")

def check_story_intelligence_no_crash():
    from agents.analytics.story_intelligence import analyze_sentiment
    result = analyze_sentiment("S1E01", {})
    assert result is None or isinstance(result, (dict, str))
    print(f"       -> analyze_sentiment stub: {type(result).__name__}")

def check_analyze_alias():
    from agents.analytics.story_intelligence import analyze, analyze_sentiment
    assert analyze == analyze_sentiment

test("analyze_sentiment no crash", check_story_intelligence_no_crash)
test("analyze alias correct",      check_analyze_alias)


# ══════════════════════════════════════════════════════════════════
# 6. A/B TRACKER
# ══════════════════════════════════════════════════════════════════
print("\n🔀 6. A/B TRACKER")

def check_ab_no_crash():
    from agents.analytics.ab_tracker import track_test
    result = track_test("S1E01")
    assert result is None or isinstance(result, (dict, str, bool))
    print(f"       -> track_test stub: {type(result).__name__}")

def check_track_ab_alias():
    from agents.analytics.ab_tracker import track_ab, track_test
    assert track_ab == track_test

test("track_test no crash",    check_ab_no_crash)
test("track_ab alias correct", check_track_ab_alias)


# ══════════════════════════════════════════════════════════════════
# 7. FULL A-12 RUN
# ══════════════════════════════════════════════════════════════════
print("\n🚀 7. FULL A-12 RUN")

def check_a12_runs():
    from orchestrator.state_schema import create_initial_state
    from agents.analytics.analytics_agent import run

    state = create_initial_state("S1E01", 1, 1, "The Weight of Crowns", "Mukut Ka Bojh")
    state["platform_outputs"] = {
        "youtube":        {"path": "output/final/S1E01_youtube.mp4",   "status": "ready"},
        "instagram_reel": {"path": "output/final/S1E01_insta.mp4",     "status": "ready"},
        "twitter":        {"path": "output/final/S1E01_twitter.mp4",   "status": "ready"},
    }
    state["formatter_ready"] = True

    result = run(state)
    assert result is not None
    print(f"       -> A-12 run completed")
    print(f"       -> State keys added: {[k for k in result.keys() if k not in state]}")

test("A-12 analytics agent runs", check_a12_runs)


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
    sys.exit(1)
else:
    print(f"\n  {PASS}  All Phase 5 checks passed. Pipeline complete.\n")
    sys.exit(0)