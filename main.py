"""
Crown of Kaliyug - Main Pipeline Entry Point
Usage:
    python main.py
    python main.py --skip-video
    python main.py --phase 1
    python main.py --episode S1E02
"""
import argparse, sys, time, os
from loguru import logger

os.makedirs("logs", exist_ok=True)
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")
logger.add("logs/pipeline_{time:YYYY-MM-DD}.log", rotation="1 day")


def run_pipeline(episode_id="S1E01", season=1, ep_num=1,
                 title_en="The Weight of Crowns", title_hi="Mukut Ka Bojh",
                 skip_video=False, phases=None):

    from orchestrator.state_schema import create_initial_state
    logger.info("="*60)
    logger.info("CROWN OF KALIYUG - PRODUCTION PIPELINE")
    logger.info(f"Episode : {episode_id} | {title_en}")
    logger.info("="*60)

    state = create_initial_state(episode_id, season, ep_num, title_en, title_hi)
    state["script_draft_path"] = f"output/scripts/{episode_id}_draft_1.json"
    start = time.time()

    # PHASE 1 - STORY ENGINE
    if phases is None or 1 in phases:
        logger.info("\n-- PHASE 1: STORY ENGINE --------------------------")

        logger.info("[1/9] A-02 Script Writer...")
        try:
            from agents.story_engine.script_writer.script_writer_agent import run as fn
            state = fn(state)
            logger.success(f"A-02 OK  {state.get('script_draft_path')}")
        except Exception as e:
            logger.error(f"A-02 FAIL  {e}")
            return state

        logger.info("[2/9] A-03 Dialogue Agent...")
        try:
            from agents.story_engine.dialogue.dialogue_agent import run as fn
            state = fn(state)
            logger.success("A-03 OK  Dialogue filled")
        except Exception as e:
            logger.warning(f"A-03 SKIP  {e}")

        logger.info("[3/9] A-04 Canon Guardian...")
        try:
            from agents.story_engine.canon_guardian.canon_guardian_agent import run as fn
            state = fn(state)
            logger.success(f"A-04 OK  {state.get('canon_result',{}).get('status','PASS')}")
        except Exception as e:
            logger.warning(f"A-04 SKIP  {e}")

    # PHASE 2 - VISUAL PRODUCTION
    if (phases is None or 2 in phases) and not skip_video:
        logger.info("\n-- PHASE 2: VISUAL PRODUCTION ---------------------")

        logger.info("[4/9] A-05 Avatar Agent...")
        try:
            from agents.visual_prod.avatar.avatar_agent import run as fn
            state = fn(state)
            logger.success("A-05 OK  Avatars mapped")
        except Exception as e:
            logger.warning(f"A-05 SKIP  {e}")

        logger.info("[5/9] A-06 Video Generation (Ken Burns ~15-20 min)...")
        try:
            from agents.visual_prod.video.video_agent import run as fn
            state = fn(state)
            logger.success(f"A-06 OK  {len(state.get('generated_clips',[]))} clips")
        except Exception as e:
            logger.warning(f"A-06 SKIP  {e}")

    elif skip_video:
        logger.warning("Phase 2 skipped")

    # PHASE 3 - AUDIO
    if phases is None or 3 in phases:
        logger.info("\n-- PHASE 3: AUDIO PRODUCTION ----------------------")

        logger.info("[6/9] A-07 Voiceover (Edge TTS)...")
        try:
            from agents.audio_prod.voiceover.voiceover_agent import run as fn
            state = fn(state)
            logger.success("A-07 OK  Voiceover done")
        except Exception as e:
            logger.warning(f"A-07 SKIP  {e}")

        logger.info("[7/9] A-08 Music Composer...")
        try:
            from agents.audio_prod.music.music_agent import run as fn
            state = fn(state)
            logger.success("A-08 OK  Music done")
        except Exception as e:
            logger.warning(f"A-08 SKIP  {e}")

        logger.info("[8/9] A-09 Sound Design...")
        try:
            from agents.audio_prod.sfx.sfx_agent import run as fn
            state = fn(state)
            logger.success("A-09 OK  SFX done")
        except Exception as e:
            logger.warning(f"A-09 SKIP  {e}")

    # PHASE 4 - POST PRODUCTION
    if phases is None or 4 in phases:
        logger.info("\n-- PHASE 4: POST PRODUCTION -----------------------")

        logger.info("[9/9] A-10 Video Editor...")
        try:
            from agents.post_prod.editor.agent import run as fn
            state = fn(state)
            logger.success(f"A-10 OK  {state.get('master_video_path')}")
        except Exception as e:
            logger.error(f"A-10 FAIL  {e}")

        if state.get("priya_shelly_approved"):
            try:
                from agents.post_prod.formatter.formatter_agent import run as fn
                state = fn(state)
                logger.success("A-11 OK  Platform cuts ready")
            except Exception as e:
                logger.warning(f"A-11 SKIP  {e}")
        else:
            logger.info("A-11 PENDING  Priya/Shelly approval needed")

    # PHASE 5 - DISTRIBUTION
    if (phases is None or 5 in phases) and state.get("formatter_ready"):
        logger.info("\n-- PHASE 5: DISTRIBUTION --------------------------")
        try:
            from agents.analytics.analytics_agent import run as fn
            state = fn(state)
            logger.success("A-12 OK  Analytics started")
        except Exception as e:
            logger.warning(f"A-12 SKIP  {e}")

    # SUMMARY
    elapsed = time.time() - start
    logger.info("\n" + "="*60)
    logger.info("PIPELINE COMPLETE")
    logger.info("="*60)
    logger.info(f"Episode    : {episode_id}")
    logger.info(f"Time taken : {int(elapsed//60)}m {int(elapsed%60)}s")
    logger.info(f"Script     : {state.get('script_draft_path','N/A')}")
    logger.info(f"Master     : {state.get('master_video_path','N/A')}")
    logger.info(f"Voiceover  : {state.get('voiceover_ready',False)}")
    logger.info(f"Music      : {state.get('music_ready',False)}")
    logger.info(f"Video clips: {state.get('video_clips_ready',False)}")
    logger.info("="*60)
    if state.get("errors"):
        logger.warning(f"Errors: {state['errors']}")
    return state


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode",    default="S1E01")
    parser.add_argument("--season",     default=1,    type=int)
    parser.add_argument("--ep-num",     default=1,    type=int)
    parser.add_argument("--title-en",   default="The Weight of Crowns")
    parser.add_argument("--title-hi",   default="Mukut Ka Bojh")
    parser.add_argument("--skip-video", action="store_true")
    parser.add_argument("--phase",      default=None, type=int)
    args   = parser.parse_args()
    phases = [args.phase] if args.phase else None
    run_pipeline(args.episode, args.season, args.ep_num,
                 args.title_en, args.title_hi, args.skip_video, phases)