"""
Crown of Kaliyug — Analytics Agent (A-12)
A-12 · agents/analytics/analytics_agent.py
"""
from loguru import logger
from agents.analytics import youtube_publisher, insta_publisher, twitter_publisher, metric_tracker, story_intelligence, weekly_report

def run(state):
    episode_id = state.get("episode_id")
    logger.info(f"[A-12] Analytics Agent — {episode_id}")
    
    # 1. Publish to platforms
    yt = youtube_publisher.publish(episode_id, state.get("yt_path"), {})
    insta = insta_publisher.publish(episode_id, state.get("insta_path"), {})
    tw = twitter_publisher.publish(episode_id, state.get("tw_path"), {})
    
    # 2. Track metrics (placeholder for first run)
    metrics = metric_tracker.fetch_metrics(episode_id)
    
    # 3. Story Intelligence
    intel = story_intelligence.analyze_sentiment(metrics, [])
    
    # 4. Final Report
    report = weekly_report.generate_report(metrics)
    
    state["analytics"] = {
        "published": [yt, insta, tw],
        "metrics": metrics,
        "sentiment": intel,
        "report": report
    }
    state["status"] = "complete"
    logger.success(f"[A-12] Done for {episode_id}")
    return state
